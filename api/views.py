from django.http import HttpResponse
from rest_framework import viewsets

from .serializers import UserSerializer, PostSerializer
from .models import User, Post


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('name')
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('user')
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        username = self.request.query_params.get('user', None)

        if username is not None:
            queryset = queryset.filter(user__name=username)
        return queryset
