from rest_framework import viewsets, mixins, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Board
from api.serializers import BoardSerializer, UserSerializer, CustomTokenObtainPairSerializer
from users.models import MyUser


class CustomPagination(PageNumberPagination):
    page_size = 4  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100


# Create your views here.
class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.order_by("-published").all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)


class RegisterView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
