from django.contrib import admin

from .models import Comment, Like, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "created_at")
    search_fields = ("author__username", "caption")
    list_filter = ("created_at",)


admin.site.register(Like)
admin.site.register(Comment)

# Register your models here.
