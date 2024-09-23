from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return data