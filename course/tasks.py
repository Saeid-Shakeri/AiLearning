from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Course

@shared_task
def send_monthly_report(recipients):
    last_month = now() - timedelta(days=30)
    courses = Course.objects.filter(date__gte=last_month)
    report = f"Monthly Report: {len(courses)} new course created."

    send_mail(
        'Monthly Report',
        report,
        'from@example.com',
        recipients,    # ['admin@example.com']
        fail_silently=False,
    )
