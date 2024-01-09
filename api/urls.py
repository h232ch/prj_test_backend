from django.urls import path, include
from rest_framework import routers
from api.views import BoardViewSet, UserViewSet, BoardCommentViewSet, BoardChildCommentViewSet, ImageViewSet, \
    CommentImageViewSet

router = routers.DefaultRouter()
router.register('boards', BoardViewSet)
router.register('comments', BoardCommentViewSet)
router.register('child_comments', BoardChildCommentViewSet)
router.register('users', UserViewSet)
router.register('images', ImageViewSet)
router.register('comment_images', CommentImageViewSet)


urlpatterns = [
    path('', include(router.urls)),
]