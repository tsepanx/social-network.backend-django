from rest_framework import viewsets

from .serializers import UserSerializer, PostSerializer
from .models import User, Post


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('author_id')
    serializer_class = PostSerializer

    def get_queryset(self):
        username = self.request.query_params.get('user', None)

        if username is not None:
            return self.queryset.filter(author__username=username)

        return self.queryset
