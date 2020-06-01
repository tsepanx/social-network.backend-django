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


class IsAdmin(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view)


def user_auth(user_field=None):
    class ModelAuthenticated(permissions.BasePermission):
        def has_permission(self, request, view):
            return True

        def has_object_permission(self, request, view, obj):
            owner_instance = obj.__getattribute__(user_field) if user_field else obj

            if not request.user:
                return False

            same_pk = owner_instance.pk == request.user.pk
            print(same_pk)

            return same_pk

    return ModelAuthenticated()


class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        pass
        # raise exceptions.AuthenticationFailed()
