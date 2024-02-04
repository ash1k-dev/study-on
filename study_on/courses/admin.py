from django.contrib import admin
from django.contrib.admin import register

from study_on.courses.models import AvailableLessons, Content, Course, Lesson, Question, Subject, Test


@register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Предметы"""

    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Курсы"""

    list_display = ("title", "slug", "subject")
    list_filter = ("subject",)


@register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Уроки"""

    list_display = ("title", "course", "order")
    list_filter = ("course",)


@register(Content)
class ContentAdmin(admin.ModelAdmin):
    """Контент"""

    list_display = ("lesson", "order")
    list_filter = ("lesson",)


@register(Test)
class TestAdmin(admin.ModelAdmin):
    """Тесты"""

    list_display = ("title", "lesson")
    list_filter = ("lesson",)


@register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Вопросы к уроку"""

    list_display = ("title", "order")
    list_filter = ("title",)


@register(AvailableLessons)
class AvailableLessonsAdmin(admin.ModelAdmin):
    """Доступные пользователю уроки курса"""

    list_display = ("course", "student", "max_available_lesson")
    list_filter = ("student",)
