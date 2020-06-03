from rest_framework import serializers

from api.models import UserProfile
from . import post


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ()


class WithPostsSerializer(ProfileSerializer):
    posts = post.PostSerializer(many=True)


class WithUsernameSerializer(ProfileSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.person.user.username


<<<<<<< HEAD
class WithPostsUsernameSerializer(WithPostsSerializer, WithUsernameSerializer):
    pass


METHOD_SERIALIZERS = {
    'list': ProfileSerializer,
    'retrieve': WithPostsUsernameSerializer,
=======
METHOD_SERIALIZERS = {
    'list': ProfileSerializer,
    'retrieve': WithPostsSerializer,
>>>>>>> 0541289 (Serializers inheritance)
    'update': ProfileSerializer
}
