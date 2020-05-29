from django.contrib.auth.models import User
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Profile
from .serializers import UserGETSerializer, UserPUTSerializer, UserSerializerWithToken, \
    PostSerializer, ProfileSerializer
from .utils import Nobody

DEFAULT_PERMISSION = (permissions.IsAuthenticatedOrReadOnly,)

USER_METHODS_SERIALIZERS = {
    'list': UserGETSerializer,
    'update': UserPUTSerializer,
    'create': UserSerializerWithToken
}

USER_METHODS_PERMISSIONS = {
    'create': (permissions.AllowAny,)
}

PROFILE_METHODS_PERMISSIONS = {
    'create': (Nobody,)
}


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserGETSerializer

    def get_permissions(self):
        permission_classes = USER_METHODS_PERMISSIONS.get(self.action, DEFAULT_PERMISSION)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        return USER_METHODS_SERIALIZERS.get(self.action, USER_METHODS_SERIALIZERS['list'])

    def update(self, request, *args, **kwargs):
        user_id = kwargs.pop('pk', None)
        password = request.data.get('password', None)

        if None not in [user_id, password]:
            user = User.objects.get(pk=user_id)
            user.set_password(password)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        permission_classes = PROFILE_METHODS_PERMISSIONS.get(self.action, DEFAULT_PERMISSION)

        return [permission() for permission in permission_classes]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('author_id')
    serializer_class = PostSerializer

    def get_queryset(self):
        profile_id = self.request.query_params.get('user', None)

        if profile_id is not None:
            return self.queryset.filter(author_id=profile_id).order_by('-pub_date')

        return self.queryset


class Me(APIView):
    """
    Current logged in user
    """

    @staticmethod
    def get(request):
        """
        Determine the current user by their token, and return their data
        """

        serializer = UserGETSerializer(request.user)
        return Response(serializer.data)
