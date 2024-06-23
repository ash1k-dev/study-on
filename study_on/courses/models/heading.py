from django.db import models
from django.utils.translation import gettext_lazy as _

from config.settings.base import MAX_DESCRIPTION_LENGTH, MAX_TITLE_LENGTH
from study_on.services.models import BaseModel


class Heading(BaseModel):
    """Модель направления"""

    title = models.CharField(max_length=MAX_TITLE_LENGTH, verbose_name=_("Направление"))
    description = models.TextField(max_length=MAX_DESCRIPTION_LENGTH, verbose_name=_("Описание"))
    is_published = models.BooleanField(default=False, verbose_name=_("Активен"))

    class Meta:
        verbose_name = _("Направление")
        verbose_name_plural = _("Направления")

    def __str__(self):
        return self.title
