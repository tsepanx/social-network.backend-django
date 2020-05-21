from rest_framework import serializers

from .models import User, Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'status', 'profile_photo', 'register_date')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'text', 'pub_date')
