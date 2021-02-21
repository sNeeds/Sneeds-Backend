from celery import shared_task
from django.utils import timezone

from abroadin.apps.notifications.models import EmailNotification, SoldTimeSlotReminderEmailNotification, \
    SoldTimeSlotChangedEmailNotification


@shared_task
def send_email_notifications():
    qs = EmailNotification.objects.filter(
        send_date__lte=timezone.now(),
        sent=False
    )

    for obj in qs:
        try:
            obj = obj.soldtimeslotreminderemailnotification
        except SoldTimeSlotReminderEmailNotification.DoesNotExist:
            pass

        try:
            obj = obj.soldtimeslotchangedemailnotification
        except SoldTimeSlotChangedEmailNotification.DoesNotExist:
            pass

    qs.update(sent=True)
