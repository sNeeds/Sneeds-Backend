from __future__ import absolute_import, unicode_literals

from celery import  shared_task

from sNeeds.utils import sendemail


@shared_task
def send_reset_password_email(email, first_name, reset_link):
    sendemail.reset_password(
        email,
        first_name,
        reset_link
    )

