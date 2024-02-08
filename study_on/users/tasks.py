from os import getenv

from django.contrib.auth import get_user_model
from django.core import mail

from config import celery_app
from study_on.users.templates import (
    TEXT_CHANGE_PASSWORD,
    TEXT_GREETING,
    TEXT_IDENTIFICATION,
    TEXT_REPEATED_IDENTIFICATION_ERROR,
)

User = get_user_model()


STUDY_ON_EMAIL = getenv("STUDY_ON_EMAIL")


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task()
def send_email(user, email_type):
    with mail.get_connection() as connection:
        email_type_dict = {
            "confirm": TEXT_IDENTIFICATION,
            "confirm_error": TEXT_REPEATED_IDENTIFICATION_ERROR,
            "change_password": TEXT_CHANGE_PASSWORD,
        }
        email_text = email_type_dict.get(email_type)
        user_name = user.username
        user_email = user.email
        subject = TEXT_GREETING.substitute(user=user_name)
        body = email_text.substitute(user=user_name, code=user.identification_code)
        mail.EmailMessage(
            subject=subject,
            body=body,
            from_email="StudyOn <" + STUDY_ON_EMAIL + ">",
            to=[user_email],
            connection=connection,
        ).send()
