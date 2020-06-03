import collections

from rest_framework import permissions


class MyNobody(permissions.BasePermission):
    def has_permission(self, request, view):
        return False


class MyIsAdmin(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view)


def user_auth(*fields):
    class ModelPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            return True

        def has_object_permission(self, request, view, obj):
            owner = obj

            if isinstance(fields, collections.Iterable) and fields:
                for f in fields:
                    owner = getattr(owner, f)

            if not request.user:
                return False

            same_pk = owner.pk == request.user.pk
            return same_pk

    return ModelPermission()


class ModelAuthenticated:
    USER = user_auth()
    PROFILE = user_auth('person', 'user')
    POST = user_auth('author', 'person', 'user')
    SOCIAL = user_auth('person', 'user')


DEFAULT_PERMISSION = permissions.IsAuthenticatedOrReadOnly()

ALLOW_ANY = permissions.AllowAny()
IS_ADMIN = MyIsAdmin()
NOBODY = MyNobody()

USER_OR_ADMIN = permissions.OR(
    ModelAuthenticated.USER,
    IS_ADMIN
)

SOCIAL_OR_ADMIN = permissions.OR(
    ModelAuthenticated.SOCIAL,
    IS_ADMIN
)

USER_METHODS_PERMISSIONS = {
    'create': [ALLOW_ANY],
    'retrieve': [USER_OR_ADMIN],
    'update': [NOBODY],
    'partial_update': [USER_OR_ADMIN],
    'destroy': [USER_OR_ADMIN]
}

PROFILE_METHODS_PERMISSIONS = {
    'create': [NOBODY],
    'update': [ModelAuthenticated.PROFILE]
}

SOCIAL_USER_METHODS_PERMISSIONS = {
    'create': [NOBODY],
    'update': [NOBODY],
    'partial_update': [SOCIAL_OR_ADMIN],
    'destroy': [SOCIAL_OR_ADMIN],
}

POST_METHODS_PERMISSIONS = {
    'create': [ModelAuthenticated.POST],
    'update': [ModelAuthenticated.POST],
}


def get_permissions_by_map(mapping, action):
    res = mapping.get(action, [DEFAULT_PERMISSION])

    return res


def viewset_permissions(viewset, perms_dict):
    return get_permissions_by_map(perms_dict, viewset.action)
