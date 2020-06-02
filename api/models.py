from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    status = models.CharField(max_length=100, blank=True)
    profile_photo = models.TextField(blank=True)

    def __str__(self):
        return self.person.__str__()


class SocialUser(models.Model):
    relationships = models.ManyToManyField('self', through='Relationship',
                                           related_name='related_to')

    def add_relationship(self, person, symmetrical=True):
        if self == person:
            return

        relationship, created = Relationship.objects.get_or_create(
            from_user=self,
            to_user=person)

        if symmetrical:
            back_relationship = person.add_relationship(self, False)
            return relationship, back_relationship

        return relationship

    def remove_relationship(self, person, symmetrical=True):
        if self == person:
            return

        Relationship.objects.filter(
            from_user=self,
            to_user=person).delete()

        if symmetrical:
            person.remove_relationship(self, False)

    def get_friends(self):
        return self.relationships.filter(following__to_user=self)

    def get_followers(self):
        return [relationship.from_user for relationship in self.followers.all()]

    def __str__(self):
        return self.person.__str__()


class Relationship(models.Model):
    from_user = models.ForeignKey(SocialUser, related_name='following', on_delete=models.CASCADE, null=True)
    to_user = models.ForeignKey(SocialUser, related_name='followers', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f'|{self.from_user.person}| -> |{self.to_user.person}|'


class Person(models.Model):
    RELATED_NAME = 'person'
    ON_DELETE = models.PROTECT

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile = models.OneToOneField(UserProfile, on_delete=ON_DELETE, related_name=RELATED_NAME)
    social_user = models.OneToOneField(SocialUser, on_delete=ON_DELETE, related_name=RELATED_NAME)

    def __str__(self):
        return self.user.__str__()


class UserManager(models.Manager):
    @staticmethod
    def create(username, password):
        user = User(username=username)

        if password is not None:
            user.set_password(password)

        user.save()

        user_profile = UserProfile.objects.create(id=user.id)
        social_user = SocialUser.objects.create(id=user.id)

        Person.objects.create(
            id=user.id,
            user=user,
            profile=user_profile,
            social_user=social_user
        )

        return user

    @staticmethod
    def delete(pk):
        to_delete = Person.objects.get(pk=pk)

        to_delete.user.delete()
        to_delete.social_user.delete()
        to_delete.profile.delete()

        Person.delete(to_delete)


class Post(models.Model):
    author = models.ForeignKey(UserProfile, related_name='posts', on_delete=models.CASCADE)

    title = models.CharField(max_length=30, default='', verbose_name='Post title')
    text = models.TextField(default='', verbose_name='Post text')

    pub_date = models.DateTimeField(verbose_name='Post published', auto_now=True)

    def __str__(self):
        return f'{self.title}, @{self.author}'


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='messages_sent')
    receiver = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name='messages_received')

    text = models.TextField(verbose_name='Message text')
    created = models.DateTimeField(auto_now_add=True)
