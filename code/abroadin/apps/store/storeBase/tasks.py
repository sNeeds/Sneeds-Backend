from celery import shared_task

from django.utils import timezone

from abroadin.utils import sib_mail_services
from .models import TimeSlotSale
from abroadin.settings.config.variables import TIME_SLOT_SALE_DELETE_TIME


@shared_task
def delete_time_slots():
    """
    Deletes time slots with less than _ hours to start.
    """
    qs = TimeSlotSale.objects.filter(
        start_time__lte=timezone.now() + timezone.timedelta(hours=TIME_SLOT_SALE_DELETE_TIME)
    )
    qs.delete()


@shared_task
def notify_sold_time_slot(send_to, name, sold_time_slot_url, start_time, end_time):
    sib_mail_services.send_sold_time_slot_email(
        send_to, name, sold_time_slot_url, start_time, end_time
    )

