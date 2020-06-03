from rest_framework import serializers

from api.models import SocialUser
from .profile import ProfileSerializer


class SocialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialUser
        fields = ('id', 'relationships')


class GETSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    def get_users(self, obj):
        for social_user in obj.relationships.all():
            yield ProfileSerializer(social_user.person.profile).data

    class Meta:
        model = SocialUser
        fields = ('id', 'users')


METHODS_SERIALIZERS = {
    'list': SocialUserSerializer,
    'retrieve': GETSerializer
}
