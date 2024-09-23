from rest_framework import serializers
from .models import User, Customer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userID', 'username', 'email', 'role', 'status', 'createdDate']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'address', 'phone']
