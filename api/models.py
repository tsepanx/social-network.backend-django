from django import forms
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=32)

    status = models.CharField(max_length=100, blank=True)
    profile_photo = models.CharField(max_length=100, blank=True)

    date_joined = models.DateField(auto_now=True)

    def posts(self):
        return Post.objects.all().filter(user__name=self.username)

    def __str__(self):
        return f'{self.username}, {self.status}'


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    title = models.CharField(max_length=30, default='', verbose_name='Post title')
    text = models.TextField(default='', verbose_name='Post text')

    pub_date = models.DateTimeField(verbose_name='Post published', auto_now=True)

    def __str__(self):
        return f'{self.title}, @{self.author.username}'
