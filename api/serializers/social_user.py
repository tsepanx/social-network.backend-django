from rest_framework import serializers

from api.models import SocialUser
from . import profile


def get_friends_of(user: SocialUser):
    for social_user in user.relationships.all():
        yield profile.WithUsernameSerializer(social_user.person.profile).data


class SocialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialUser
        exclude = ('person',)


class RetrieveSerializer(SocialUserSerializer):
    friends = serializers.SerializerMethodField()

    def get_friends(self, obj):
        return get_friends_of(obj)

    class Meta(SocialUserSerializer.Meta):
        exclude = ('relationships', 'person')


METHODS_SERIALIZERS = {
    'list': SocialUserSerializer,
    'retrieve': RetrieveSerializer
}
