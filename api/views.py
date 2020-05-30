from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Profile
from .serializers import user, profile, post

# from .user import UserGETSerializer, UserPUTSerializer, UserSerializerWithToken
# from .user.post import PostSerializer
# from .user.profile import ProfileSerializer, ProfileWithPostsSerializer
from .utils import Nobody, user_auth

ProfileAuthenticated = user_auth('user')
PostAuthenticated = user_auth('author')

DEFAULT_PERMISSION = (permissions.IsAuthenticatedOrReadOnly,)

USER_METHODS_PERMISSIONS = {
    'create': (permissions.AllowAny,)
}

PROFILE_METHODS_PERMISSIONS = {
    'create': (Nobody,),
    'update': (ProfileAuthenticated,)
}

POST_METHODS_PERMISSIONS = {
    'create': (PostAuthenticated,),
    'update': (PostAuthenticated,),
}


def get_permissions_by_map(mapping, action):
    permission_classes = mapping.get(action, DEFAULT_PERMISSION)

    return [permission() for permission in permission_classes]


def get_serializer_by_map(mapping, action):
    default_serializer = mapping.get('list')

    return mapping.get(action, default_serializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = user.GETSerializer

    def get_permissions(self):
        return get_permissions_by_map(USER_METHODS_PERMISSIONS, self.action)

    def get_serializer_class(self):
        return get_serializer_by_map(user.METHODS_SERIALIZERS, self.action)

    def update(self, request, *args, **kwargs):
        user_id = kwargs.pop('pk', None)

        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if user_id:
            user = User.objects.get(pk=user_id)

            if password:
                user.set_password(password)
            if username:
                user.username = username

            user.save()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = profile.ProfileSerializer

    def get_serializer_class(self):
        return get_serializer_by_map(profile.METHOD_SERIALIZERS, self.action)

    def get_permissions(self):
        return get_permissions_by_map(PROFILE_METHODS_PERMISSIONS, self.action)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('author_id')
    serializer_class = post.PostSerializer

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

        serializer = user.GETSerializer(request.user)
        return Response(serializer.data)
