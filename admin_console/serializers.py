#serializers.py

from rest_framework import serializers
from .models import User_Reg

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Reg
        fields = '__all__'

