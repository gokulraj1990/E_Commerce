from rest_framework import serializers
from .models import CustomerProfile
from admin_console.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password', 'email', 'status', 'createdDate']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['user', 'address', 'phone']
