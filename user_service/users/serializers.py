from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'phone', 'address', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=15, required=False)
    address = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'phone', 'address']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']

    def create(self, validated_data):
        phone = validated_data.pop('phone', '')
        address = validated_data.pop('address', '')
        
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, phone=phone, address=address)
        return user
