from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from . import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'posts', views.PostViewSet)
from .views import current_user, UserList

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token-auth/', obtain_jwt_token),

    path('me/', current_user),
    path('users/', UserList.as_view())
]

