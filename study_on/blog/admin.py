from django.contrib import admin
from django.contrib.admin import register

from study_on.blog.models import Content, Post


@register(Post)
class PostAdmin(admin.ModelAdmin):
    """Посты"""

    list_display = ("title", "author", "slug")
    prepopulated_fields = {"slug": ("title",)}


@register(Content)
class ContentAdmin(admin.ModelAdmin):
    """Контент"""

    list_display = ("id", "post", "order", "is_published")
    list_filter = ("post",)
