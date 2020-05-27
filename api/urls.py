from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

from .views import current_user, UserList

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token-auth/', obtain_jwt_token),

    path('me/', current_user),
    path('users/', UserList.as_view())
]

