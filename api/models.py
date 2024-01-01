from django.contrib.auth.models import User, AbstractUser
from django.db import models

from users.models import MyUser


class Board(models.Model):
    title = models.CharField(max_length=36, null=False)
    content = models.TextField(max_length=256, blank=True, null=False)
    published = models.DateTimeField(null=True)
    user = models.ForeignKey(MyUser, related_name='boards', on_delete=models.CASCADE, null=True)

    # it would express title on admin site
    def __str__(self):
        return self.title


class BoardComment(models.Model):
    board = models.ForeignKey(Board, related_name='comments', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=256)
    published = models.DateTimeField(null=True)


