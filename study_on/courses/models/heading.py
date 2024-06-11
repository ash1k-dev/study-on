from django.db import models
from django.utils.translation import gettext_lazy as _

from study_on.services.models import BaseModel


class Heading(BaseModel):
    """Модель направления"""

    title = models.CharField(max_length=200, verbose_name=_("Направление"))
    description = models.TextField(verbose_name=_("Описание"))
    is_published = models.BooleanField(default=False, verbose_name=_("Активен"))

    class Meta:
        verbose_name = _("Направление")
        verbose_name_plural = _("Направления")

    def __str__(self):
        return self.title
