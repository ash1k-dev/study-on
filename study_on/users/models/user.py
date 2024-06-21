from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for study_on.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(blank=True, max_length=255, verbose_name=_("Имя пользователя"))
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    reward = models.ManyToManyField("users.Reward", blank=True, related_name="users", verbose_name=_("Награда"))
    identification_code = models.IntegerField(default=0, verbose_name=_("Код для подтверждения пользователя"))
    identification_code_entry_attempts = models.IntegerField(default=0, verbose_name=_("Попытки ввода кода"))

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
