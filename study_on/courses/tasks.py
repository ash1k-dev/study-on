from datetime import datetime, timedelta
from os import getenv

from django.core import mail
from django.db.models import Q

from config import celery_app
from study_on.courses.models import AvailableLessons
from study_on.courses.templates import TEXT_GREETING, TEXT_REMINDER

STUDY_ON_EMAIL = getenv("STUDY_ON_EMAIL", default="test_mail@localhost")
COURSE_REMINDER_DAYS = getenv("COURSE_REMINDER_DAYS", default=3)

celery_app.conf.beat_schedule = {
    "add-every-30-seconds": {
        "task": "study_on.courses.tasks.course_reminder",
        "schedule": timedelta(days=COURSE_REMINDER_DAYS),
        "args": (),
    },
}


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
    with mail.get_connection() as connection:
        for result in uinited_results:
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
