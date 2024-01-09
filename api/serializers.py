from typing import Dict, Any

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import Board, BoardComment, BoardChildComment, Image, CommentImage
from users.models import MyUser


class BoardChildCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = BoardChildComment
        # fields = ['id', 'user', 'email', 'comment', 'published', 'p_comment']
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image',]


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = ['id', 'image',]


class BoardCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    email = serializers.EmailField(source='user.email', read_only=True)
    child_comments = BoardChildCommentSerializer(many=True, read_only=True)
    comment_images = CommentImageSerializer(many=True, read_only=True)

    class Meta:
        model = BoardComment
        fields = ['id', 'user', 'email', 'board', 'comment', 'published', 'child_comments', 'comment_images']
        # fields = '__all__'

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')

        comment = BoardComment.objects.create(**validated_data)
        for image_data in images_data:
            CommentImage.objects.create(comment=comment, image=image_data)
        return comment

    def update(self, instance, validated_data):
        # Update board instance fields
        instance.comment = validated_data.get('comment', instance.comment)
        # Add other board fields that need updating
        instance.save()

        # Handle image updates
        if 'request' in self.context:
            images_data = self.context['request'].FILES.getlist('images')

            # You can choose different strategies here. For example:
            # 1. Clear existing images and add new ones:
            # instance.images.all().delete()
            # 2. Add new images to existing ones:
            # 3. Update existing images (more complex, requires identifying images)

            # This example follows option 2: adding new images to existing ones
            for image_data in images_data:
                CommentImage.objects.create(comment=instance, image=image_data)

        return instance


class BoardSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    email = serializers.EmailField(source='user.email', read_only=True)
    comments = BoardCommentSerializer(many=True, read_only=True)
    board_images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'user', 'email', 'title', 'content', 'published', 'comments', 'board_images']

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')

        board = Board.objects.create(**validated_data)
        for image_data in images_data:
            Image.objects.create(board=board, image=image_data)
        return board

    def update(self, instance, validated_data):
        # Update board instance fields
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        # Add other board fields that need updating
        instance.save()

        # Handle image updates
        if 'request' in self.context:
            images_data = self.context['request'].FILES.getlist('images')

            # You can choose different strategies here. For example:
            # 1. Clear existing images and add new ones:
            # instance.images.all().delete()
            # 2. Add new images to existing ones:
            # 3. Update existing images (more complex, requires identifying images)

            # This example follows option 2: adding new images to existing ones
            for image_data in images_data:
                Image.objects.create(board=instance, image=image_data)

        return instance


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

