from django.contrib import admin

from .models import User, Post


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'status', 'date_joined')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'text')
