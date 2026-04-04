from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role':     {'required': False},
        }

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'viewer')
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
      class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'date_joined']
        read_only_fields = ['id', 'username', 'email', 'role', 'date_joined']