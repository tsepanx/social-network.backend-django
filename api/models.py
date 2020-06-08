from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()


class UserProfile(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='profile', null=True)

    status = models.CharField(max_length=100, blank=True)
    profile_photo = models.TextField(blank=True)

    def __str__(self):
        return self.person.__str__()


class SocialUser(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='social_user', null=True)

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


class UserManager(models.Manager):
    @staticmethod
    def create(username, password):
        user = User(username=username)

        if password is not None:
            user.set_password(password)

        user.save()

        person = Person.objects.create(
            id=user.id,
            user=user,
        )

        params = {
            'id': user.id,
            'person': person
        }

        UserProfile.objects.create(**params)
        SocialUser.objects.create(**params)

        return user


class Post(models.Model):
    author = models.ForeignKey(UserProfile, related_name='posts', on_delete=models.CASCADE)

    title = models.CharField(max_length=30, default='', verbose_name='Post title')
    text = models.TextField(default='', verbose_name='Post text')

    pub_date = models.DateTimeField(verbose_name='Post published', auto_now=True)

    def __str__(self):
        return f'{self.title}, @{self.author}'


class Chat(models.Model):
    participants = models.ManyToManyField(Person, related_name='chats')

    def is_participant(self, person):
        return person in self.participants.all()

    def add_participant(self, person):
        return self.participants.add(person)

    def remove_participant(self, person):
        if self.is_participant(person):
            self.participants.remove(person)
        else:
            raise Exception("User doesn't exist")

    def send_message(self, from_person: Person, text):
        if self.is_participant(from_person):
            msg = Message.objects.create(
                sender=from_person,
                chat=self,
                text=text
            )

            return msg
        raise Exception('User not in chat')

    def __str__(self):
        return f'Messages: {len(self.messages.all())}'


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', default=None)
    sender = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='sent_messages')

    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}: {self.text}'
