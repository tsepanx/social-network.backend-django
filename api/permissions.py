from rest_framework import permissions


class MyNobody(permissions.BasePermission):
    def has_permission(self, request, view):
        return False


class MyIsAdmin(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view)


def user_auth(user_field=None):
    class ModelPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            return True

        def has_object_permission(self, request, view, obj):
            if user_field == 'person__user':  # TODO doesn't work with that field, set it manually
                owner = obj.person.user
            elif user_field:
                owner = obj.__getattribute__(user_field)
            else:
                owner = obj

            if not request.user:
                return False

            same_pk = owner.pk == request.user.pk
            return same_pk

    return ModelPermission()


class ModelAuthenticated:
    USER = user_auth(None)
    PROFILE = user_auth('person__user')
    POST = user_auth('author__person__user')


DEFAULT_PERMISSION = permissions.IsAuthenticatedOrReadOnly()

ALLOW_ANY = permissions.AllowAny()
IS_ADMIN = MyIsAdmin()
NOBODY = MyNobody()

USER_OR_ADMIN = permissions.OR(
    ModelAuthenticated.USER,
    IS_ADMIN
)

USER_METHODS_PERMISSIONS = {
    'create': [ALLOW_ANY],
    'update': [USER_OR_ADMIN],
    'retrieve': [USER_OR_ADMIN],
    'destroy': [USER_OR_ADMIN]
}

PROFILE_METHODS_PERMISSIONS = {
    'create': [NOBODY],
    'update': [ModelAuthenticated.PROFILE]
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
