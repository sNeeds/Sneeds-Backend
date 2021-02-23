from celery import shared_task
from django.utils import timezone

from abroadin.apps.notifications.models import EmailNotification


@shared_task
def send_email_notifications():
    qs = EmailNotification.objects.filter(
        send_date__lte=timezone.now(),
        sent=False
    )
