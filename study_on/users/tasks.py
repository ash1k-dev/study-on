from django.contrib.auth import get_user_model
from django.core import mail

from config import celery_app
from study_on.services.email import create_email_text, send_email

User = get_user_model()


@celery_app.task()
def send_email_task(
    username, email, email_type, lesson=None, reward=None, identification_code=None, course_title=None
):
    with mail.get_connection() as connection:
        body, subject = create_email_text(course_title, email_type, identification_code, lesson, reward, username)
        send_email(body, connection, email, subject)
