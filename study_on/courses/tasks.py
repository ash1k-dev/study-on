from datetime import datetime, timedelta

from django.core import mail
from django.db.models import Q

from config import celery_app
from config.settings.base import COURSE_REMINDER_DAYS, STUDY_ON_EMAIL
from study_on.courses.models import AvailableLessons
from study_on.courses.templates import TEXT_GREETING, TEXT_REMINDER

celery_app.conf.beat_schedule = {
    "add-every-3-days": {
        "task": "study_on.courses.tasks.course_reminder",
        "schedule": timedelta(days=COURSE_REMINDER_DAYS),
        "args": (),
    },
}


@celery_app.task()
def course_reminder():
    """Напоминание студентам о незаконченом курсе"""
    united_results = (
        AvailableLessons.objects.all()
        .select_related("student", "course")
        .filter(Q(updated__lt=datetime.now() - timedelta(days=3)))
    )
    with mail.get_connection() as connection:
        for result in united_results:
            student = result.student.username
            student_email = result.student.email
            course_name = result.course.title
            subject = TEXT_GREETING.substitute(student=student)
            body = TEXT_REMINDER.substitute(student=student, course_name=course_name)
            mail.EmailMessage(
                subject=subject,
                body=body,
                from_email="StudyOn <" + STUDY_ON_EMAIL + ">",
                to=[student_email],
                connection=connection,
            ).send()
