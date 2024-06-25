from datetime import datetime, timedelta

from django.core import mail
from django.db.models import Q

from config import celery_app
from config.settings.base import COURSE_REMINDER_DAYS
from study_on.courses.models import AvailableLessons
from study_on.services.email import create_email_text, send_email

celery_app.conf.beat_schedule = {
    "add-every-3-days": {
        "task": "study_on.courses.tasks.course_reminder",
        "schedule": timedelta(days=COURSE_REMINDER_DAYS),
        "args": (),
    },
}


@celery_app.task()
def course_reminder_task():
    """Напоминание студентам о незаконченном курсе"""
    united_results = (
        AvailableLessons.objects.all()
        .select_related("student", "course")
        .filter(Q(updated__lt=datetime.now() - timedelta(days=3)))
    )
    with mail.get_connection() as connection:
        for result in united_results:
            username = result.student.username
            email = result.student.email
            course_title = result.course.title
            email_type = "reminder"
            body, subject = create_email_text(course_title, username, email_type)
            send_email(body, connection, email, subject)
