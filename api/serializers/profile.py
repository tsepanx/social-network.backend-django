from rest_framework import serializers

from api.models import Profile
from . import user, post


class ProfileSerializer(serializers.ModelSerializer):
    user = user.ProfileUserSerializer(read_only=True)

    class Meta:
        model = Profile
        exclude = ()  # ('id',)


class ProfileWithPostsSerializer(ProfileSerializer):
    posts = post.PostSerializer(many=True)


METHOD_SERIALIZERS = {
    'list': ProfileSerializer,
    'retrieve': ProfileWithPostsSerializer,
    'update': ProfileSerializer
}
