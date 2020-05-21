from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=100, blank=True)
    profile_photo = models.CharField(max_length=100, blank=True)

    register_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'@{self.name}, status: {self.status}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    title = models.CharField(max_length=30, default='', verbose_name='Post title')
    text = models.TextField(verbose_name='Post text')

    pub_date = models.DateTimeField(verbose_name='Post published', auto_now=True)

    def __str__(self):
        return f'@{self.user.name}, {self.title}, {self.pub_date}'
