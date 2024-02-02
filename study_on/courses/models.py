from django.db import models
from django.utils.translation import gettext_lazy as _

from study_on.courses.fields import OrderField


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Subject(BaseModel):
    title = models.CharField(max_length=200, verbose_name=_("Заголовок"))
    description = models.TextField(verbose_name=_("Описание"))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Ссылка"))

    class Meta:
        verbose_name = _("Предмет")
        verbose_name_plural = _("Предметы")

    def __str__(self):
        return self.title


class Course(BaseModel):
    subject = models.ForeignKey(
        "courses.Subject", related_name="courses", on_delete=models.CASCADE, verbose_name=_("Предмет")
    )
    teachers = models.ManyToManyField(
        "users.User", related_name="courses_teachers", blank=True, verbose_name=_("Преподаватели")
    )
    students = models.ManyToManyField(
        "users.User", related_name="courses_joined", blank=True, verbose_name=_("Студенты")
    )
    title = models.CharField(max_length=200, verbose_name=_("Заголовок"))
    description = models.TextField(max_length=500, verbose_name=_("Описание"))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Ссылка"))

    class Meta:
        verbose_name = _("Курс")
        verbose_name_plural = _("Курсы")

    def __str__(self):
        return self.title


class Lesson(BaseModel):
    course = models.ForeignKey(
        "courses.Course", related_name="lessons", on_delete=models.CASCADE, verbose_name=_("Курс")
    )
    title = models.CharField(max_length=200, verbose_name=_("Заголовок"))
    description = models.TextField(max_length=500, verbose_name=_("Описание"))
    order = OrderField(blank=True, for_fields=["course"], verbose_name=_("Порядок"))

    class Meta:
        verbose_name = _("Урок")
        verbose_name_plural = _("Уроки")

    def __str__(self):
        return self.title


class Content(BaseModel):
    lesson = models.ForeignKey(
        "courses.Lesson", related_name="contents", on_delete=models.CASCADE, verbose_name=_("Урок")
    )
    text = models.TextField(verbose_name=_("Текст"))
    video = models.URLField(blank=True, verbose_name=_("Видео"))
    image = models.FileField(upload_to="images", blank=True, verbose_name=_("Изображение"))
    order = OrderField(blank=True, for_fields=["lesson"], verbose_name=_("Порядок"))

    class Meta:
        verbose_name = _("Содержание")
        verbose_name_plural = _("Содержание")

    def __str__(self):
        return self.text


class Test(BaseModel):
    lesson = models.ForeignKey(
        "courses.Lesson", related_name="tests", on_delete=models.CASCADE, verbose_name=_("Урок")
    )
    title = models.CharField(max_length=200, verbose_name=_("Заголовок"))
    description = models.TextField(max_length=500, verbose_name=_("Описание"))
    answer_check = models.BooleanField(default=False, verbose_name=_("Правильность"))

    class Meta:
        verbose_name = _("Тест")
        verbose_name_plural = _("Тесты")

    def __str__(self):
        return self.title


class Question(BaseModel):
    test = models.ForeignKey(
        "courses.Test", related_name="questions", on_delete=models.CASCADE, verbose_name=_("Тест")
    )
    title = models.CharField(max_length=200, verbose_name=_("Заголовок"))
    question_text = models.TextField(max_length=400, verbose_name=_("Текст вопроса"))
    answer_text = models.TextField(max_length=500, blank=True, verbose_name=_("Текст ответа"))
    answer_check = models.BooleanField(default=False, verbose_name=_("Правильность"))
    order = OrderField(blank=True, for_fields=["test"], verbose_name=_("Порядок"))

    class Meta:
        verbose_name = _("Вопрос")
        verbose_name_plural = _("Вопросы")

    def __str__(self):
        return self.title


class AvailableLessons(BaseModel):
    course = models.ForeignKey(
        "courses.Course", related_name="student", on_delete=models.CASCADE, verbose_name=_("Курс")
    )
    student = models.ForeignKey(
        "users.User", related_name="available_lessons", on_delete=models.CASCADE, verbose_name=_("Студент")
    )
    max_available_lesson = models.PositiveIntegerField(
        default=0,
        help_text=_(
            "Номер урока",
        ),
        verbose_name=_("Доступный урок"),
    )

    class Meta:
        verbose_name = _("Доступные уроки курса")
        verbose_name_plural = _("Доступные уроки курса")
        unique_together = ["course", "student"]

    def __str__(self):
        return self.course
