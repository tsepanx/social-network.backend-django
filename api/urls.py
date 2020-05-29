from django.conf.urls import url
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

from . import views
from .router import DefaultRouterWithSimpleViews

router = DefaultRouterWithSimpleViews()
router.register(r'post', views.PostViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'me', views.Me, 'me')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_jwt_token),

    path('rest-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

