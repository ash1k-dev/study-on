from django.db import models
from django.utils.translation import gettext_lazy as _

from study_on.services.models import BaseModel


class Bookmark(BaseModel):
    """Модель закладок"""

    course = models.ForeignKey(
        "courses.Course",
        related_name="bookmarks",
        on_delete=models.CASCADE,
        verbose_name=_("Курс"),
    )
    student = models.ForeignKey(
        "users.User",
        related_name="bookmarks",
        on_delete=models.CASCADE,
        verbose_name=_("Студент"),
    )

    class Meta:
        verbose_name = _("Закладка")
        verbose_name_plural = _("Закладки")
        unique_together = ["course", "student"]

    def __str__(self):
        return f"{self.course} - {self.student}"
