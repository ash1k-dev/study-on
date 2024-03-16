from django.db import models


class BaseModel(models.Model):
    """Базовая модель, c полями даты создания и обновления"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
