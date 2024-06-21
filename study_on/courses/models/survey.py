from django.db import models
from django.utils.translation import gettext_lazy as _

from study_on.services.models import BaseModel


class Survey(BaseModel):
    """Модель теста для урока"""

    lesson = models.ForeignKey(
        to="courses.Lesson",
        related_name="surveys",
        on_delete=models.CASCADE,
        verbose_name=_("Урок"),
    )
    title = models.CharField(max_length=200, verbose_name=_("Заголовок"))
    description = models.TextField(max_length=500, verbose_name=_("Описание"))
    is_published = models.BooleanField(default=False, verbose_name=_("Активен"))

    class Meta:
        verbose_name = _("Тест")
        verbose_name_plural = _("Тесты")
        constraints = [models.UniqueConstraint(fields=["lesson"], name="unique_survey_per_lesson")]

    def __str__(self):
        return self.title
