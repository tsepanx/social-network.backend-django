from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    status = models.CharField(max_length=100, blank=True)
    profile_photo = models.CharField(max_length=100, blank=True)

    def posts(self):
        return Post.objects.all().filter(author=self)

    def __str__(self):
        return f'{self.user.username}, {self.status}'


class UserManager(models.Manager):
    @staticmethod
    def create(username, password):
        user = User(username=username)

        if password is not None:
            user.set_password(password)

        user.save()

        profile = Profile(id=user.id, user=user)
        profile.save()
        return user

    @staticmethod
    def delete(profile_id):
        pass  # TODO


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    title = models.CharField(max_length=30, default='', verbose_name='Post title')
    text = models.TextField(default='', verbose_name='Post text')

    pub_date = models.DateTimeField(verbose_name='Post published', auto_now=True)

    def __str__(self):
        return f'{self.title}, @{self.author.user.username}'
