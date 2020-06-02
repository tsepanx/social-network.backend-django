from django.contrib import admin
from .models import Post, UserProfile, SocialUser, Person


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_photo', 'status')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'text')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile', 'social_user',)


@admin.register(SocialUser)
class SocialUserAdmin(admin.ModelAdmin):
    list_display = ('person',)
