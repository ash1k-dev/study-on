from django.db import models
from django.utils.translation import gettext_lazy as _

from config.settings.base import MAX_DESCRIPTION_LENGTH, MAX_TITLE_LENGTH
from study_on.services.fields import OrderField
from study_on.services.models import BaseModel


class Lesson(BaseModel):
    """Модель урока"""

    course = models.ForeignKey(
        to="courses.Course",
        related_name="lessons",
        on_delete=models.CASCADE,
        verbose_name=_("Курс"),
    )
    title = models.CharField(max_length=MAX_TITLE_LENGTH, verbose_name=_("Заголовок"))
    description = models.TextField(max_length=MAX_DESCRIPTION_LENGTH, verbose_name=_("Описание"))
    order = OrderField(blank=True, for_fields=["course"], verbose_name=_("Порядок"))
    is_published = models.BooleanField(default=False, verbose_name=_("Активен"))

    class Meta:
        verbose_name = _("Урок")
        verbose_name_plural = _("Уроки")

    def __str__(self):
        return self.title
