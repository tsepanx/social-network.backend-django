from django.contrib import admin

from .models import User, Post


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'text')
