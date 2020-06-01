from rest_framework import serializers

from api.models import UserProfile
from . import user, post


class ProfileSerializer(serializers.ModelSerializer):
    user = user.UserProfileSerializer(read_only=True)

    class Meta:
        model = UserProfile
        exclude = ()  # ('id',)


class ProfileWithPostsSerializer(ProfileSerializer):
    posts = post.PostSerializer(many=True)


METHOD_SERIALIZERS = {
    'list': ProfileSerializer,
    'retrieve': ProfileWithPostsSerializer,
    'update': ProfileSerializer
}
