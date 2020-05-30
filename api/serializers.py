from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User

from api.models import Post, Profile, UserManager


class UserGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserPUTSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)

        return UserManager.create(
            username=username,
            password=password
        )

    class Meta:
        model = User
        fields = ('token', 'username', 'password')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = ProfileUserSerializer(read_only=True)

    class Meta:
        model = Profile
        exclude = ()  # ('id',)


class ProfileWithPostsSerializer(ProfileSerializer):
    posts = PostSerializer(many=True)
