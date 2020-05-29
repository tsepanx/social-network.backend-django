from rest_framework import permissions

from .serializers import UserGETSerializer


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserGETSerializer(user, context={'request': request}).data
    }


class Nobody(permissions.BasePermission):
    def has_permission(self, request, view):
        return False


class ProfileAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, profile):
        profile_user = profile.user

        if not request.user:
            return False

        return profile_user == request.user or request.user.is_staff
