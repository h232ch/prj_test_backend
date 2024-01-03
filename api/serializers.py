from typing import Dict, Any

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import Board, BoardComment, BoardChildComment
from users.models import MyUser


class BoardChildCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = BoardChildComment
        # fields = {'id', 'user', 'child_comments', 'published'}
        # fields = ['id', 'user', 'email', 'comment', 'published', 'p_comment']
        fields = ('__all__')


class BoardCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    email = serializers.EmailField(source='user.email', read_only=True)
    child_comments = BoardChildCommentSerializer(many=True, read_only=True)

    class Meta:
        model = BoardComment
        fields = ['id', 'user', 'email', 'board', 'comment', 'published', 'child_comments']


class BoardSerializer(serializers.ModelSerializer):
    # the user field should be changed like board comment serializer
    user = serializers.ReadOnlyField(source='user.id')
    email = serializers.EmailField(source='user.email', read_only=True)
    comments = BoardCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'user', 'email', 'title', 'content', 'published', 'comments']


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

