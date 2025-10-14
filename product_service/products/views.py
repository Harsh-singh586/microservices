from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from .models import Product, Category
from .serializers import ProductSerializer, ProductListSerializer, CategorySerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductSerializer
        return ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(['GET'])
def product_by_id(request, product_id):
    """API endpoint to get product by ID - used by other services"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def check_stock(request):
    """API endpoint to check product stock - used by other services"""
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        if product.stock_quantity >= quantity:
            return Response({
                'available': True, 
                'product_name': product.name,
                'price': product.price,
                'stock_quantity': product.stock_quantity
            })
        else:
            return Response({
                'available': False, 
                'message': f'Only {product.stock_quantity} items available'
            }, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_stock(request):
    """API endpoint to update product stock - used by other services"""
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')
    operation = request.data.get('operation', 'decrease')  # 'increase' or 'decrease'
    
    try:
        product = Product.objects.get(id=product_id)
        
        if operation == 'decrease':
            if product.stock_quantity >= quantity:
                product.stock_quantity -= quantity
                product.save()
                return Response({'success': True, 'new_stock': product.stock_quantity})
            else:
                return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
        elif operation == 'increase':
            product.stock_quantity += quantity
            product.save()
            return Response({'success': True, 'new_stock': product.stock_quantity})
        else:
            return Response({'error': 'Invalid operation'}, status=status.HTTP_400_BAD_REQUEST)
            
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
