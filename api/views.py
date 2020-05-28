from django.contrib.auth.models import User
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Profile
from .serializers import UserSerializer, UserSerializerWithToken, PostSerializer, ProfileSerializer


class Me(APIView):
    """
    Current logged in user
    """

    @staticmethod
    def get(request):
        """
        Determine the current user by their token, and return their data
        """

        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user, or list existing users.
    """

    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def get(request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('author_id')
    serializer_class = PostSerializer

    def get_queryset(self):
        username = self.request.query_params.get('user', None)

        if username is not None:
            return self.queryset.filter(author__user__id=username)

        return self.queryset
