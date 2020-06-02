from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, UserProfile, SocialUser, Person

from .serializers import user, profile, post, social_user
from .permissions import viewset_permissions, \
    USER_METHODS_PERMISSIONS, \
    PROFILE_METHODS_PERMISSIONS, \
    POST_METHODS_PERMISSIONS


def get_serializer_by_map(mapping, action):
    default_serializer = mapping.get('list')

    return mapping.get(action, default_serializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = user.GETSerializer

    def get_permissions(self):
        return viewset_permissions(self, USER_METHODS_PERMISSIONS)

    def get_serializer_class(self):
        return get_serializer_by_map(user.METHODS_SERIALIZERS, self.action)

    def update(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        instance = self.get_object()

        if username and password:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=False)

            instance.username = username
            instance.set_password(password)
        elif username:
            instance.username = username
        elif password:
            instance.set_password(password)

        instance.save()

        response_serializer = self.get_serializer(instance)
        return Response(response_serializer.data)

    def destroy(self, request, *args, **kwargs):
        Person.objects.get(pk=kwargs.pop('pk')).delete()

        return Response()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = profile.ProfileSerializer

    def get_serializer_class(self):
        return get_serializer_by_map(profile.METHOD_SERIALIZERS, self.action)

    def get_permissions(self):
        return viewset_permissions(self, PROFILE_METHODS_PERMISSIONS)


class SocialUserViewSet(viewsets.ModelViewSet):
    queryset = SocialUser.objects.all()

    def get_serializer_class(self):
        return get_serializer_by_map(social_user.METHODS_SERIALIZERS, self.action)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('author_id')
    serializer_class = post.PostSerializer

    def get_permissions(self):
        return viewset_permissions(self, POST_METHODS_PERMISSIONS)

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
