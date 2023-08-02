from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, UserPost, Comment


class MyUserAdmin(admin.ModelAdmin):
    list_display = ["username", "about", "first_name", "last_name", "email", "is_staff"]
    # fieldsets = [
    #     ("User name", {"fields": ["username"]}),
    #     ("About", {"fields": ["about"]}),
    #     ("Email", {"fields": ["email"]})
    # ]


@admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin):
    # list_display = ["title", "description", "body"]
    list_display = ["title", "content"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # list_display = ('name', 'body', 'post', 'created_on')
    list_display = ['name', 'post', 'created_on']
    list_filter = ['created_on',]
    # search_fields = ('name', 'email', 'body')
    search_fields = ['name']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(MyUser, MyUserAdmin)
