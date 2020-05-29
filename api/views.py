from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Profile
from .serializers import UserGETSerializer, UserPUTSerializer, UserSerializerWithToken, \
    PostSerializer, ProfileSerializer
from .utils import Nobody, ProfileAuthenticated

DEFAULT_PERMISSION = (permissions.IsAuthenticatedOrReadOnly,)

USER_METHODS_SERIALIZERS = {
    'list': UserGETSerializer,
    'update': UserPUTSerializer,
    'create': UserSerializerWithToken
}

USER_METHODS_PERMISSIONS = {
    'create': (permissions.AllowAny,)
}

PROFILE_METHOD_SERIALIZERS = {
    'list': ProfileSerializer,
    'update': ProfileSerializer
}

PROFILE_METHODS_PERMISSIONS = {
    'create': (Nobody,),
    'update': (ProfileAuthenticated,)
}

POST_METHODS_PERMISSIONS = {
    'create': (ProfileAuthenticated,),
    'update': (ProfileAuthenticated,),
}


def get_permissions_by_map(mapping, action):
    permission_classes = mapping.get(action, DEFAULT_PERMISSION)

    return [permission() for permission in permission_classes]


def get_serializer_by_map(mapping, action):
    default_serializer = mapping.get('list')

    return mapping.get(action, default_serializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserGETSerializer

    def get_permissions(self):
        return get_permissions_by_map(USER_METHODS_PERMISSIONS, self.action)

    def get_serializer_class(self):
        return get_serializer_by_map(USER_METHODS_SERIALIZERS, self.action)

    def update(self, request, *args, **kwargs):
        user_id = kwargs.pop('pk', None)
        password = request.data.get('password', None)

        if None not in [user_id, password]:
            user = User.objects.get(pk=user_id)
            user.set_password(password)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_serializer_class(self):
        return get_serializer_by_map(PROFILE_METHOD_SERIALIZERS, self.action)

    def get_permissions(self):
        return get_permissions_by_map(PROFILE_METHODS_PERMISSIONS, self.action)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('author_id')
    serializer_class = PostSerializer

    def get_permissions(self):
        return get_permissions_by_map(POST_METHODS_PERMISSIONS, self.action)

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
