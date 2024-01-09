from django.contrib.auth.models import User, AbstractUser
from django.db import models
import os
import uuid
from users.models import MyUser


def hashed_upload_to(instance, filename):
    extension = filename.split('.')[-1]
    hashed_filename = f"{uuid.uuid4().hex}.{extension}"
    user_id = instance.board.user.id if instance.board.user else 'unknown user'
    return os.path.join('images/boards', str(user_id), hashed_filename)


def comment_hashed_upload_to(instance, filename):
    extension = filename.split('.')[-1]
    hashed_filename = f"{uuid.uuid4().hex}.{extension}"
    user_id = instance.comment.user.id if instance.comment.user else 'unknown user'
    return os.path.join('images/boards', str(user_id), hashed_filename)


class Board(models.Model):
    title = models.CharField(max_length=36, null=False)
    content = models.TextField(max_length=256, blank=True, null=False)
    published = models.DateTimeField(null=True)
    user = models.ForeignKey(MyUser, related_name='boards', on_delete=models.CASCADE, null=True)
    images = models.ManyToManyField('Image', related_name='board_images', blank=True)

    def __str__(self):
        return self.title


class BoardComment(models.Model):
    board = models.ForeignKey(Board, related_name='comments', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=256)
    published = models.DateTimeField(null=True)
    images = models.ManyToManyField('CommentImage', related_name='comment_images', blank=True)


class BoardChildComment(models.Model):
    p_comment = models.ForeignKey(BoardComment, related_name='child_comments', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=256)
    published = models.DateTimeField(null=True)


class Image(models.Model):
    board = models.ForeignKey(Board, related_name='board_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=hashed_upload_to, null=True, blank=True)


class CommentImage(models.Model):
    comment = models.ForeignKey(BoardComment, related_name='comment_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=comment_hashed_upload_to, null=True, blank=True)

