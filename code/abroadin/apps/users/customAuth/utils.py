from celery import shared_task

from django.contrib.auth import get_user_model

from verification.conf import VERIFICATION_CODE_FIELD

from abroadin.utils.sendemail import (send_verification_code_email,
                                      create_sib_contact,
                                      update_sib_contact,
                                      create_sib_doi_contact, perform_appropriate_lists,
                                      MARKETING_LIST, DOI_LIST)

User = get_user_model()


def user_creation_email_handling(instance: User):
    create_contact.delay(instance)


def user_update_email_handling(instance: User, db_instance: User):
    if instance.receive_marketing_email != db_instance.receive_marketing_email:
        update_contact.delay(instance)
    if instance.is_email_verified != db_instance.is_email_verified:
        update_contact.delay(instance)


@shared_task()
def create_contact(user: User):
    create_sib_contact(user.email, first_name=user.first_name, last_name=user.last_name,
                       phone_number=user.phone_number, opt_in=user.is_email_verified,
                       lists=perform_appropriate_lists(user))


@shared_task()
def update_contact(user: User):
    update_sib_contact(user.email, first_name=user.first_name, last_name=user.last_name,
                       phone_number=user.phone_number, opt_in=user.is_email_verified,
                       lists=perform_appropriate_lists(user))


@shared_task()
def create_doi_contact(email, phone_number, **kwargs):
    assert email or phone_number, (
        'User must enter at least Email or Phone number for subscription.'
    )
    create_sib_doi_contact(email, phone_number=phone_number, lists=[MARKETING_LIST, DOI_LIST], **kwargs)


def send_verification_code(view, request, verification):
    user = verification.user
    email = user.email
    code = getattr(verification, VERIFICATION_CODE_FIELD)
    full_name = user.get_pretty_full_name()
    verification_type = verification.verification_type

    if verification_type == 'email':
        send_email_verification_task.delay(email_address=email, full_name=full_name, code=code)


@shared_task()
def send_email_verification_task(email_address, full_name, code):
    if code is None or len(code) == 0:
        raise Exception("Code is None or empty string")
    return send_verification_code_email(send_to=email_address, full_name=full_name, code=code)
