from django.contrib import admin

from study_on.courses.models import (
    AvailableLessons,
    Bookmark,
    Completion,
    Content,
    Course,
    Heading,
    Lesson,
    Question,
    Review,
    Subject,
    Survey,
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Предметы"""

    list_display = ("id", "title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Курсы"""

    list_display = ("id", "title", "slug", "subject")
    list_filter = ("subject",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Уроки"""

    list_display = ("id", "title", "course", "order")
    list_filter = ("course",)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """Контент"""

    list_display = ("id", "lesson", "order")
    list_filter = ("lesson",)


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    """Тесты"""

    list_display = ("id", "title", "lesson")
    list_filter = ("lesson",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Вопросы к уроку"""

    list_display = ("id", "title", "order")
    list_filter = ("title",)


@admin.register(AvailableLessons)
class AvailableLessonsAdmin(admin.ModelAdmin):
    """Доступные пользователю уроки курса"""

    list_display = ("id", "course", "student", "max_available_lesson")
    list_filter = ("student",)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """Закладки"""

    list_display = ("id", "course", "student")
    list_filter = ("course", "student")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""

    list_display = ("id", "course", "student", "grade")
    list_filter = ("course", "student")


@admin.register(Heading)
class HeadingAdmin(admin.ModelAdmin):
    """Направления"""

    list_display = ("id", "title")
    list_filter = ("title",)


@admin.register(Completion)
class CompletionAdmin(admin.ModelAdmin):
    """Завершенный курс"""

    list_display = ("id", "course", "user")
    list_filter = ("course", "user")
