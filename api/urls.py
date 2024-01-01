from django.urls import path, include
from rest_framework import routers
from api.views import BoardViewSet, UserViewSet, BoardCommentSet

router = routers.DefaultRouter()
router.register('boards', BoardViewSet)
router.register('comments', BoardCommentSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]