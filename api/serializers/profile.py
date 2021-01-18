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


class WithPostsUsernameSerializer(WithPostsSerializer, WithUsernameSerializer):
    pass


class RetrieveSerializer(WithPostsUsernameSerializer):
    friends = serializers.SerializerMethodField()

    def get_friends(self, obj):
        su = obj.person.social_user
        return social_user.get_friends_of(su)


METHOD_SERIALIZERS = {
    'list': WithUsernameSerializer,
    'retrieve': RetrieveSerializer,
    'update': ProfileSerializer
}
