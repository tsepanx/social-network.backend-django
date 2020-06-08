from rest_framework import serializers

from api.models import UserProfile
from . import post, social_user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('person',)


class WithPostsSerializer(ProfileSerializer):
    posts = post.PostSerializer(many=True)


class WithUsernameSerializer(ProfileSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.person.user.username


<<<<<<< HEAD
class WithPostsUsernameSerializer(WithPostsSerializer, WithUsernameSerializer):
    pass


class RetrieveSerializer(WithPostsUsernameSerializer):
    friends = serializers.SerializerMethodField()

    def get_friends(self, obj):
        su = obj.person.social_user
        return social_user.get_friends_of(su)


METHOD_SERIALIZERS = {
<<<<<<< HEAD
    'list': ProfileSerializer,
    'retrieve': WithPostsUsernameSerializer,
=======
METHOD_SERIALIZERS = {
    'list': ProfileSerializer,
    'retrieve': WithPostsSerializer,
>>>>>>> 0541289 (Serializers inheritance)
=======
    'list': WithUsernameSerializer,
    'retrieve': RetrieveSerializer,
>>>>>>> 5d8ebcc (friends field for retrieve of profile)
    'update': ProfileSerializer
}
