from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(read_only=True)  # Will be populated from Product Service
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_info = serializers.JSONField(read_only=True)  # Will be populated from User Service
    
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'user_info', 'status', 'total_amount', 
                 'shipping_address', 'items', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    
    class Meta:
        model = Order
        fields = ['user_id', 'shipping_address', 'items']
        
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Calculate total amount
        total_amount = sum(item['quantity'] * item['price'] for item in items_data)
        
        order = Order.objects.create(total_amount=total_amount, **validated_data)
        
        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        return order
