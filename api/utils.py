from rest_framework import permissions, authentication

from . import serializers


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': serializers.user.GETSerializer(user, context={'request': request}).data
    }


class Nobody(permissions.BasePermission):
    def has_permission(self, request, view):
        return False


def user_auth(user_field):
    class ModelAuthenticated(permissions.BasePermission):
        def has_permission(self, request, view):
            return True

        def has_object_permission(self, request, view, obj):
            owner_instance = obj.__getattribute__(user_field)

            if not request.user:
                return False

            same_username = owner_instance.username == request.user.username
            is_staff = request.user.is_staff

            return same_username or is_staff

    return ModelAuthenticated


class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        pass
        # raise exceptions.AuthenticationFailed()
