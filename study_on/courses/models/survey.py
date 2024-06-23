from django.db import models
from django.utils.translation import gettext_lazy as _

from config.settings.base import MAX_DESCRIPTION_LENGTH, MAX_TITLE_LENGTH
from study_on.services.models import BaseModel


class Survey(BaseModel):
    """Модель теста для урока"""

    lesson = models.ForeignKey(
        to="courses.Lesson",
        related_name="surveys",
        on_delete=models.CASCADE,
        verbose_name=_("Урок"),
    )
    title = models.CharField(max_length=MAX_TITLE_LENGTH, verbose_name=_("Заголовок"))
    description = models.TextField(max_length=MAX_DESCRIPTION_LENGTH, verbose_name=_("Описание"))
    is_published = models.BooleanField(default=False, verbose_name=_("Активен"))

    class Meta:
        verbose_name = _("Тест")
        verbose_name_plural = _("Тесты")
        constraints = [models.UniqueConstraint(fields=["lesson"], name="unique_survey_per_lesson")]

    def __str__(self):
        return self.title
