from django.db import models
from django.utils.translation import gettext_lazy as _

from study_on.services.models import BaseModel


class Course(BaseModel):
    """Модель курса"""

    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        blank=True,
        default=None,
        verbose_name=_("Автор"),
    )
    subject = models.ForeignKey(
        "courses.Subject", related_name="courses", on_delete=models.CASCADE, verbose_name=_("Предмет")
    )
    teachers = models.ManyToManyField(
        "users.User",
        related_name="courses_teachers",
        blank=True,
        verbose_name=_("Преподаватели"),
    )
    students = models.ManyToManyField(
        "users.User",
        related_name="courses_joined",
        blank=True,
        verbose_name=_("Студенты"),
    )
    completed_students = models.ManyToManyField(
        "users.User",
        related_name="completed_courses",
        through="courses.Completion",
        blank=True,
        verbose_name=_("Завершившие курс"),
    )
    title = models.CharField(max_length=200, verbose_name=_("Заголовок"))
    description = models.TextField(max_length=500, verbose_name=_("Описание"))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Ссылка"))
    is_published = models.BooleanField(default=False, verbose_name=_("Активен"))

    class Meta:
        verbose_name = _("Курс")
        verbose_name_plural = _("Курсы")

    def __str__(self):
        return self.title