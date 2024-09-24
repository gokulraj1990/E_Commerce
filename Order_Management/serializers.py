from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['orderID', 'customerID', 'productID', 'quantity', 'totalPrice', 'orderDate', 'status']
        read_only_fields = ['orderID', 'totalPrice', 'orderDate']

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return data