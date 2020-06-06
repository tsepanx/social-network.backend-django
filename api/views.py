from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, UserProfile, SocialUser, Person

from .serializers import user, profile, post, social_user
from .permissions import viewset_permissions, \
    USER_METHODS_PERMISSIONS, \
    PROFILE_METHODS_PERMISSIONS, \
    POST_METHODS_PERMISSIONS, \
    SOCIAL_USER_METHODS_PERMISSIONS


def get_serializer_by_map(mapping, action):
    default_serializer = mapping.get('list')

    return mapping.get(action, default_serializer)


def my_viewset(permissions_mapping, serializers_mapping):
    class MyViewSet(viewsets.ModelViewSet):
        def get_permissions(self):
            return viewset_permissions(self, permissions_mapping)

        def get_serializer_class(self):
            return get_serializer_by_map(serializers_mapping, self.action)

    return MyViewSet


class UserViewSet(my_viewset(USER_METHODS_PERMISSIONS, user.METHODS_SERIALIZERS)):
    queryset = User.objects.all()
    serializer_class = user.GETSerializer

    def partial_update(self, request, *args, **kwargs):
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


class ProfileViewSet(my_viewset(PROFILE_METHODS_PERMISSIONS, profile.METHOD_SERIALIZERS)):
    queryset = UserProfile.objects.all()


class SocialUserViewSet(my_viewset(SOCIAL_USER_METHODS_PERMISSIONS, social_user.METHODS_SERIALIZERS)):
    queryset = SocialUser.objects.all()

    def handle_relationship(self, request, *args, **kwargs):
        from_id = kwargs.get('pk', None)
        to_id = request.query_params.get('to', None)

        symmetrical = request.query_params.get('symmetrical', False)

        if to_id:
            from_social_user = SocialUser.objects.get(id=from_id)
            to_social_user = SocialUser.objects.get(id=to_id)

            if self.action == 'partial_update':
                from_social_user.add_relationship(to_social_user, symmetrical)
            elif self.action == 'destroy':
                from_social_user.remove_relationship(to_social_user, symmetrical)

    def update(self, request, *args, **kwargs):
        return self.handle_relationship(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.handle_relationship(request, *args, **kwargs)


class PostViewSet(my_viewset(POST_METHODS_PERMISSIONS, post.METHODS_SERIALIZERS)):
    queryset = Post.objects.all().order_by('-pub_date')

    def get_queryset(self):
        profile_id = self.request.query_params.get('user', None)

        if profile_id is not None:
            return self.queryset.filter(author_id=profile_id)
        return super().get_queryset()


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
