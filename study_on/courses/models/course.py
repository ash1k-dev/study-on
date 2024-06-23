from django.db import models
from django.utils.translation import gettext_lazy as _

from config.settings.base import MAX_DESCRIPTION_LENGTH, MAX_TITLE_LENGTH
from study_on.services.models import BaseModel


class Course(BaseModel):
    """Модель курса"""

    author = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        verbose_name=_("Автор"),
    )
    subject = models.ForeignKey(
        to="courses.Subject", related_name="courses", on_delete=models.CASCADE, verbose_name=_("Предмет")
    )
    teachers = models.ManyToManyField(
        to="users.User",
        related_name="courses_teachers",
        blank=True,
        verbose_name=_("Преподаватели"),
    )
    students = models.ManyToManyField(
        to="users.User",
        related_name="courses_joined",
        blank=True,
        verbose_name=_("Студенты"),
    )
    completed_students = models.ManyToManyField(
        to="users.User",
        related_name="completed_courses",
        through="courses.Completion",
        blank=True,
        verbose_name=_("Завершившие курс"),
    )
    title = models.CharField(max_length=MAX_TITLE_LENGTH, verbose_name=_("Заголовок"))
    description = models.TextField(max_length=MAX_DESCRIPTION_LENGTH, verbose_name=_("Описание"))
    slug = models.SlugField(unique=True, verbose_name=_("Ссылка"))
    is_published = models.BooleanField(default=False, verbose_name=_("Активен"))

    class Meta:
        verbose_name = _("Курс")
        verbose_name_plural = _("Курсы")

    def __str__(self):
        return self.title
