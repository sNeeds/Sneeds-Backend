from celery import shared_task

from abroadin.utils import mail_services


@shared_task
def notify_order_created(email, name, order_url):
    mail_services.send_order_created_email(email, name, order_url)
