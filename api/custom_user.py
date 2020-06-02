from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        pass

    def create_superuser(self, email, date_of_birth, password=None):
        pass


class MyUser(User):
    # pass
    objects = MyUserManager()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser
        fields = UserCreationForm.Meta.fields
