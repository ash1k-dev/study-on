from django.db import models
from django.utils.translation import gettext_lazy as _

from study_on.services.models import BaseModel


class Completion(BaseModel):
    """Модель отметки о завершении курса"""

    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="completions",
        verbose_name=_("Курс"),
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="completions",
        verbose_name=_("Пользователь"),
    )

    class Meta:
        verbose_name = _("Завершенный курс")
        verbose_name_plural = _("Завершенные курсы")
        constraints = [models.UniqueConstraint(fields=["course", "user"], name="unique_completion")]
