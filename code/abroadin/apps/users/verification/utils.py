from celery import shared_task

from django.contrib.auth import get_user_model

from verification.conf import VERIFICATION_CODE_FIELD

from abroadin.utils.sendemail import send_verification_code_email

User = get_user_model()


def send_email_verification(*args, **kwargs):
    user_id = kwargs.get('user')
    user = User.objcet.get(id=user_id)
    email = user.email
    code = kwargs.get(VERIFICATION_CODE_FIELD)
    full_name = user.get_full_name()
    send_email_verification_task.delay(email_address=email, full_name=full_name, code=code)


@shared_task()
def send_email_verification_task(email_address, full_name, code):
    send_verification_code_email(send_to=email_address, full_name=full_name, code=code)