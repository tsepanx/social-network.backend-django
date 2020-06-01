from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    status = models.CharField(max_length=100, blank=True)
    profile_photo = models.CharField(max_length=100, blank=True)

    relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False,
                                           related_name='related_to')

    def add_relationship(self, person):
        relationship, created = Relationship.objects.get_or_create(
            from_person=self,
            to_person=person)
        return relationship

    def remove_relationship(self, person):
        Relationship.objects.filter(
            from_person=self,
            to_person=person).delete()
        return

    def __str__(self):
        return f'{self.user.username}, {self.status}'


class Relationship(models.Model):
    from_person = models.ForeignKey(Profile, related_name='from_people', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Profile, related_name='to_people', on_delete=models.DO_NOTHING)


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
    author = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)

    title = models.CharField(max_length=30, default='', verbose_name='Post title')
    text = models.TextField(default='', verbose_name='Post text')

    pub_date = models.DateTimeField(verbose_name='Post published', auto_now=True)

    def __str__(self):
        return f'{self.title}, @{self.author.user.username}'


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages_sent')
    receiver = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='messages_received')

    text = models.TextField(verbose_name='Message text')
    created = models.DateTimeField(auto_now_add=True)
