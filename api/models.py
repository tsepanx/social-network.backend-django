from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=100)
    profile_photo = models.CharField(max_length=100)

    register_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'@{self.username}, status: {self.status}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    title = models.CharField(max_length=30, default='', verbose_name='Post title')
    text = models.TextField(verbose_name='Post text')

    pub_date = models.DateTimeField(verbose_name='Post published', auto_now=True)

    def __str__(self):
        return f'@{self.user.username}, {self.title}, {self.pub_date}'
