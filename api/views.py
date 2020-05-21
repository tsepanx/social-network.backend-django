from django.http import HttpResponse
from rest_framework import viewsets

from .serializers import UserSerializer, PostSerializer
from .models import User, Post


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('user')
    serializer_class = PostSerializer
