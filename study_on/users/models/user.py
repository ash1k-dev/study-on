from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from config.settings.base import MAX_NAME_LENGTH


class User(AbstractUser):
    """Модель пользователя"""

    name = CharField(blank=True, max_length=MAX_NAME_LENGTH, verbose_name=_("Имя пользователя"))
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    notification_permission = models.BooleanField(default=True, verbose_name=_("Уведомления"))
    reward = models.ManyToManyField(to="users.Reward", blank=True, related_name="users", verbose_name=_("Награда"))
    identification_code = models.IntegerField(default=0, verbose_name=_("Код для подтверждения пользователя"))
    identification_code_entry_attempts = models.IntegerField(default=0, verbose_name=_("Попытки ввода кода"))

    def get_absolute_url(self) -> str:
        """Получение ссылки для пользователя"""
        return reverse("users:detail", kwargs={"username": self.username})
