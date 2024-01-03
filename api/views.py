from django.db.models import Q
from rest_framework import viewsets, mixins, generics, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Board, BoardComment, BoardChildComment
from api.permissions import IsOwnerOrReadOnly
from api.serializers import BoardSerializer, UserSerializer, CustomTokenObtainPairSerializer, BoardCommentSerializer, \
    BoardChildCommentSerializer
from users.models import MyUser


class CustomPagination(PageNumberPagination):
    page_size = 5  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.order_by("-published").all()
    authentication_classes = (JWTAuthentication,)
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser)
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def search_data(self, request):
        search = request.data.get('search')
        type = request.data.get('type')

        if not search:
            return Response({'detail': 'Please provide search_data in the request data.'},
                            status=status.HTTP_400_BAD_REQUEST)

        queryset = Board.objects.filter(
            Q(title__icontains=search)
        ).order_by("-published")

        if type == 'title':
            # queryset = Board.objects.filter(title__icontains=search).order_by("-published")
            queryset = Board.objects.filter(
                Q(title__icontains=search)
            ).order_by("-published")
        elif type == 'title/content':
            queryset = Board.objects.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            ).order_by("-published")
        elif type == 'user':
            # queryset = Board.objects.filter(
            #     user__email__icontains=search
            # ).order_by("-published")
            queryset = Board.objects.filter(user__email__exact=search).order_by("-published")

        # Paginate the queryset
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


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


class BoardCommentViewSet(viewsets.ModelViewSet):
    queryset = BoardComment.objects.order_by("-published").all()
    serializer_class = BoardCommentSerializer
    authentication_classes = (JWTAuthentication,)
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BoardChildCommentViewSet(viewsets.ModelViewSet):
    queryset = BoardChildComment.objects.order_by("-published").all()
    serializer_class = BoardChildCommentSerializer
    authentication_classes = (JWTAuthentication,)
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)