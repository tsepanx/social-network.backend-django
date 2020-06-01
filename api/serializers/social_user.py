from rest_framework import serializers

from api.models import SocialUser


class SocialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialUser
        fields = '__all__'


METHODS_SERIALIZERS = {
    'list': SocialUserSerializer,
}
