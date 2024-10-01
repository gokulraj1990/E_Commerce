from rest_framework import serializers
from .models import CustomerProfile

class CustomerProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)  # Include user ID

    class Meta:
        model = CustomerProfile
        fields = ['user_id', 'mobile_number', 'address', 'city', 'state', 'country']  # Ensure user_id is in fields
