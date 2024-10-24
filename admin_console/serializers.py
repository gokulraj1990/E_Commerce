from rest_framework import serializers
from .models import User,Admin
from django.contrib.auth.hashers import make_password



class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','firstname', 'lastname', 'email', 'mobilenumber', 'password', 'role', 'account_status', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class AdminRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['firstname', 'lastname', 'email', 'mobilenumber', 'password', 'role', 'account_status', 'admin_code']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        admin = Admin(**validated_data)
        admin.save()
        return admin

    def validate_email(self, value):
        if Admin.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
