from __future__ import absolute_import, unicode_literals

from celery import  shared_task

from abroadin.utils import mail_services


@shared_task
def send_reset_password_email(email, full_name, reset_link):
    mail_services.send_reset_password_email(
        email,
        full_name,
        reset_link
    )

