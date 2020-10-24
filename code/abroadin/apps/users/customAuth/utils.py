from celery import shared_task

from django.contrib.auth import get_user_model

from verification.conf import VERIFICATION_CODE_FIELD

from abroadin.utils.sendemail import send_verification_code_email

User = get_user_model()


def send_verification_code(view, request, verification):
    user = verification.user
    email = user.email
    code = getattr(verification, VERIFICATION_CODE_FIELD)
    full_name = user.get_full_name()
    verification_type = verification.verification_type

    if verification_type == 'email':
        # print(user)
        # print(code)
        send_email_verification_task.delay(email_address=email, full_name=full_name, code=code)


@shared_task()
def send_email_verification_task(email_address, full_name, code):
    send_verification_code_email(send_to=email_address, full_name=full_name, code=code)