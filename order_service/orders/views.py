from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer
from .services import ExternalServiceClient


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_queryset(self):
        queryset = Order.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Enrich orders with user and product information
        for order_data in serializer.data:
            # Get user info
            user_info = ExternalServiceClient.get_user_info(order_data['user_id'])
            order_data['user_info'] = user_info
            
            # Get product info for each item
            for item in order_data.get('items', []):
                product_info = ExternalServiceClient.get_product_info(item['product_id'])
                if product_info:
                    item['product_name'] = product_info.get('name', 'Unknown Product')
        
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Validate user exists
        user_info = ExternalServiceClient.get_user_info(serializer.validated_data['user_id'])
        if not user_info:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate products and stock
        items_data = serializer.validated_data['items']
        validated_items = []
        
        for item_data in items_data:
            product_id = item_data['product_id']
            quantity = item_data['quantity']
            
            # Check if product exists and has sufficient stock
            stock_info = ExternalServiceClient.check_product_stock(product_id, quantity)
            if not stock_info or not stock_info.get('available'):
                return Response({
                    'error': f'Product {product_id} is not available or insufficient stock'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update price from current product price
            item_data['price'] = stock_info['price']
            validated_items.append(item_data)
        
        # Create order with transaction
        try:
            with transaction.atomic():
                # Create the order
                order = serializer.save()
                
                # Update stock for all products
                for item_data in validated_items:
                    success = ExternalServiceClient.update_product_stock(
                        item_data['product_id'], 
                        item_data['quantity'], 
                        'decrease'
                    )
                    if not success:
                        raise Exception(f"Failed to update stock for product {item_data['product_id']}")
                
                # Return created order with enriched data
                response_serializer = OrderSerializer(order)
                order_data = response_serializer.data
                
                # Enrich with user info
                order_data['user_info'] = user_info
                
                # Enrich items with product names
                for i, item in enumerate(order_data['items']):
                    product_info = ExternalServiceClient.get_product_info(item['product_id'])
                    if product_info:
                        item['product_name'] = product_info.get('name', 'Unknown Product')
                
                return Response(order_data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        order_data = serializer.data
        
        # Enrich with user info
        user_info = ExternalServiceClient.get_user_info(order_data['user_id'])
        order_data['user_info'] = user_info
        
        # Enrich items with product names
        for item in order_data.get('items', []):
            product_info = ExternalServiceClient.get_product_info(item['product_id'])
            if product_info:
                item['product_name'] = product_info.get('name', 'Unknown Product')
        
        return Response(order_data)


@api_view(['POST'])
def cancel_order(request, order_id):
    """Cancel an order and restore stock"""
    try:
        order = Order.objects.get(id=order_id)
        
        if order.status in ['delivered', 'cancelled']:
            return Response({
                'error': 'Cannot cancel order with status: ' + order.status
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Restore stock for all items
        for item in order.items.all():
            ExternalServiceClient.update_product_stock(
                item.product_id, 
                item.quantity, 
                'increase'
            )
        
        # Update order status
        order.status = 'cancelled'
        order.save()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
