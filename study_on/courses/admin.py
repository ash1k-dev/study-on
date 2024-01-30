from django.contrib import admin
from django.contrib.admin import register

from .models import Content, Course, Lesson, Question, Subject, Test


@register(Subject)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "subject")
    list_filter = ("subject",)


@register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)


@register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("lesson", "order")
    list_filter = ("lesson",)


@register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson")
    list_filter = ("lesson",)


@register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_filter = ("title",)
