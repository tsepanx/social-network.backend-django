from rest_framework import serializers

from .models import User, Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'status', 'profile_photo', 'date_joined')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'text', 'pub_date')
