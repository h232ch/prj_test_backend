from typing import Dict, Any

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, User, update_last_login
from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import Board
from users.models import MyUser


class BoardSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'user', 'email', 'title', 'content', 'published',]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'password']
        # Password needs to be only writable and required
        # Below code makes UserSerializer doesn't show the password anymore
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            }
        }

    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add the user ID to the response data
        user = self.user
        data['id'] = user.id
        data['email'] = user.email

        return data

