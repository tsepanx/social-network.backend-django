from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

from . import views
from .router import DefaultRouterWithSimpleViews

router = DefaultRouterWithSimpleViews()
router.register(r'posts', views.PostViewSet)
router.register(r'users', views.UserList, 'users')
router.register(r'me', views.Me, 'me')

urlpatterns = [
    path('', include(router.urls)),
    path('token-auth/', obtain_jwt_token),
]

