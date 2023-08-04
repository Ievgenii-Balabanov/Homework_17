from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, UserPost, Comment


class ItemInLine(admin.StackedInline):
    model = Comment
    extra = 1


class MyUserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "is_staff"]
    # fieldsets = [
    #     ("User name", {"fields": ["username"]}),
    #     ("About", {"fields": ["about"]}),
    #     ("Email", {"fields": ["email"]})
    # ]


@admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "summary", "content", "status"]
    search_fields = ["title"]
    list_filter = ["created_on"]
    list_select_related = True

    inlines = [ItemInLine]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created_on', "is_published"]
    list_filter = ['created_on']
    search_fields = ['name']
    actions = ['approve_comments']
    ordering = ["-created_on"]

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(MyUser, MyUserAdmin)
