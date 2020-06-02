from rest_framework import permissions, authentication


class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        pass
        # raise exceptions.AuthenticationFailed()
