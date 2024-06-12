from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from study_on.services.models import BaseModel
from study_on.users.models import Reward
from study_on.users.tasks import send_email


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


@receiver(post_save, sender=Completion)
def check_reward(sender, instance, created, **kwargs):
    """Получение награды за прохождение курса"""
    if created:
        completion_count = Completion.objects.filter(user=instance.user).count()
        if completion_count == 1:
            reward = Reward.objects.get(title="За прохождение первого курса")
            instance.user.reward.add(reward)
            send_email.delay(instance.user.username, instance.user.email, reward.title, "reward")
        elif completion_count == 5:
            reward = Reward.objects.get(title="За прохождение пяти курсов")
            instance.user.reward.add(reward)
            send_email.delay(instance.user.username, instance.user.email, reward.title, "reward")
        elif completion_count == 10:
            reward = Reward.objects.get(title="За прохождение десяти курсов")
            instance.user.reward.add(reward)
            send_email.delay(instance.user.username, instance.user.email, reward.title, "reward")