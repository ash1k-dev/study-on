import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

from django.db.models import Q

from config import celery_app
from study_on.courses.models import AvailableLessons

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_EMAIL = "your_email"
SMTP_PASSWORD = "your_password"


def get_email_user_template(student, student_email, course_name):
    email = EmailMessage()
    email["Subject"] = "Ваш курс ждет Вас!"
    email["From"] = "StudyOn <" + SMTP_EMAIL + ">"
    email["To"] = student_email

    email.set_content(
        "<div>"
        f'<h1>Здравствуйте, {student}, Вы давно не посещали курс "{course_name}"</h1>'
        "Возвращайтесь, мы Вас ждем!"
        "</div>",
        subtype="html",
    )
    return email


@celery_app.task()
def course_reminder():
    uinited_results = (
        AvailableLessons.objects.all()
        .prefetch_related("student")
        .prefetch_related(
            "course",
        )
        .filter(Q(updated__lt=datetime.now() - timedelta(days=3)))
    )
    for result in uinited_results:
        student = result.student.username
        student_email = result.student.email
        course_name = result.course.title
        email = get_email_user_template(student, student_email, course_name)
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(email)
