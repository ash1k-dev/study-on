from django.db import models
from django.utils.translation import gettext_lazy as _

from study_on.services.fields import OrderField
from study_on.services.models import BaseModel


class Content(BaseModel):
    """Модель содержания для урока"""

    lesson = models.ForeignKey(
        "courses.Lesson",
        related_name="contents",
        on_delete=models.CASCADE,
        verbose_name=_("Урок"),
    )
    text = models.TextField(verbose_name=_("Текст"))
    video = models.URLField(blank=True, verbose_name=_("Видео"))
    image = models.FileField(upload_to="images", blank=True, verbose_name=_("Изображение"))
    order = OrderField(blank=True, for_fields=["lesson"], verbose_name=_("Порядок"))
    is_published = models.BooleanField(default=False, verbose_name=_("Активен"))

    class Meta:
        verbose_name = _("Содержание")
        verbose_name_plural = _("Содержание")

    def __str__(self):
        return self.text
