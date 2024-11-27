from rest_framework import serializers
from .models import CartItem, Order, OrderItem, WishlistItem
from product_mgmt.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    productname = serializers.CharField(source='product.productname')
    price = serializers.FloatField(source='product.price')
    model = serializers.CharField(source='product.model')
    description = serializers.CharField(source='product.description', required=False)
    imageUrl = serializers.CharField(source='product.imageUrl', required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'productname', 'price', 'model', 'description', 'imageUrl', 'quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Nested serializer for order items

    class Meta:
        model = Order
        fields = ['order_id', 'user', 'created_at', 'total_amount', 'is_paid', 'address', 'city', 'pincode', 'items']

    def create(self, validated_data):
        items_data = self.context['request'].data.get('items', [])
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

class WishListSerializer(serializers.ModelSerializer):
    productname = serializers.CharField(source='product.productname')
    price = serializers.FloatField(source='product.price')
    model = serializers.CharField(source='product.model')
    description = serializers.CharField(source='product.description', required=False)
    imageUrl = serializers.CharField(source='product.imageUrl', required=False)

    class Meta:
        model = WishlistItem
        fields = ['id', 'productname', 'price', 'model', 'description', 'imageUrl']