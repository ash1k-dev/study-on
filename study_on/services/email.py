from django.core import mail

from config.settings.base import STUDY_ON_EMAIL
from study_on.courses.templates import TEXT_REMINDER
from study_on.users.templates import (
    TEXT_CHANGE_PASSWORD,
    TEXT_GREETING,
    TEXT_IDENTIFICATION,
    TEXT_REPEATED_IDENTIFICATION_ERROR,
    TEXT_REWARD,
    TEXT_SURVEY_APPROVE,
    TEXT_SURVEY_DONE,
)

email_type_dict = {
    "confirm": TEXT_IDENTIFICATION,
    "confirm_error": TEXT_REPEATED_IDENTIFICATION_ERROR,
    "change_password": TEXT_CHANGE_PASSWORD,
    "reward": TEXT_REWARD,
    "survey_approve": TEXT_SURVEY_APPROVE,
    "survey_done": TEXT_SURVEY_DONE,
    "reminder": TEXT_REMINDER,
}


def send_email(body, connection, email, subject):
    mail.EmailMessage(
        subject=subject,
        body=body,
        from_email="StudyOn <" + STUDY_ON_EMAIL + ">",
        to=[email],
        connection=connection,
    ).send()


def create_email_text(email_type, username, identification_code=None, lesson=None, reward=None, course_title=None):
    email_text_template = email_type_dict.get(email_type)
    subject = TEXT_GREETING.substitute(user=username)
    if email_type == "reward":
        body = email_text_template.substitute(user=username, reward=reward)
    elif email_type == "survey_approve":
        body = email_text_template.substitute(user=username, lesson=lesson)
    elif email_type == "survey_done":
        body = email_text_template.substitute(user=username, lesson=lesson)
    elif email_type == "reminder":
        body = email_text_template.substitute(user=username, course_name=course_title)
    else:
        body = email_text_template.substitute(user=username, code=identification_code)
    return body, subject
