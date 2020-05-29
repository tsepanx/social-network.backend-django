from .serializers import UserGETSerializer


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserGETSerializer(user, context={'request': request}).data
    }
