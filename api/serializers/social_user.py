from rest_framework import serializers

from api.models import SocialUser
from . import profile


class SocialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialUser
        exclude = ()


class RetrieveSerializer(SocialUserSerializer):
    list = serializers.SerializerMethodField()

    def get_list(self, obj):
        for social_user in obj.relationships.all():
            yield profile.WithUsernameSerializer(social_user.person.profile).data

    class Meta(SocialUserSerializer.Meta):
        exclude = ('relationships',)


METHODS_SERIALIZERS = {
    'list': SocialUserSerializer,
    'retrieve': RetrieveSerializer
}
