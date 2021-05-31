from celery import shared_task

from django.contrib.auth import get_user_model

from verification.conf import VERIFICATION_CODE_FIELD

from abroadin.utils.pakat_mail_services import (send_verification_code_email,
                                                create_pakat_contact,
                                                update_pakat_contact,
                                                WEBSITE_LIST,
                                                SUBSCRIBE_DOI_LIST,
                                                create_pakat_doi_contact, MY_DESTINATION_CAMPAIGN_LIST
                                                )

User = get_user_model()


def user_creation_handle_contact(instance: User):
    create_contact_inductor(instance)


def user_update_handle_contact(instance: User, db_instance: User):
    # print('user_update_handle_contact')
    # print(instance.receive_marketing_email)
    if instance.receive_marketing_email != db_instance.receive_marketing_email:
        create_contact_inductor(instance)
        update_contact_inductor(instance)
    elif instance.is_email_verified != db_instance.is_email_verified:
        create_contact_inductor(instance)
        update_contact_inductor(instance)


def create_contact_inductor(user):
    phone_number = None if user.phone_number is None else str(user.phone_number)
    create_contact.delay(user.email, first_name=user.first_name, last_name=user.last_name,
                         phone_number=phone_number, opt_in=user.is_email_verified,
                         receive_marketing_email=user.receive_marketing_email,
                         lists=[WEBSITE_LIST, MY_DESTINATION_CAMPAIGN_LIST])


@shared_task()
def create_contact(email, *args, **kwargs):
    phone_number = kwargs.get('phone_number')
    assert email, (
        'User must enter Email for subscription.'
    )
    assert phone_number is None or (isinstance(phone_number, str) and phone_number != 'None'), (
        'Phone number should be None or string'
    )
    return create_pakat_contact(email, *args, **kwargs)


def update_contact_inductor(user):
    phone_number = None if user.phone_number is None else str(user.phone_number)
    update_contact.delay(user.email, first_name=user.first_name, last_name=user.last_name,
                         phone_number=phone_number, opt_in=user.is_email_verified,
                         receive_marketing_email=user.receive_marketing_email,
                         lists=[WEBSITE_LIST, MY_DESTINATION_CAMPAIGN_LIST])


@shared_task()
def update_contact(email, *args, **kwargs):
    # print('update_contact')
    # print(kwargs.get('receive_marketing_email'))
    return update_pakat_contact(email, *args, **kwargs)


@shared_task()
def create_doi_contact(email, phone_number, **kwargs):
    assert email or phone_number, (
        'User must enter at least Email or Phone number for subscription.'
    )
    assert email, (
        'User must enter Email for subscription.'
    )
    assert phone_number is None or (isinstance(phone_number, str) and phone_number != 'None'), (
        'Phone number should be None or string'
    )
    return create_pakat_doi_contact(email, phone_number=phone_number, lists=[SUBSCRIBE_DOI_LIST], **kwargs)


def check_email_assigned_to_user(email):
    qs = User.objects.filter(email__iexact=email)
    return qs.exists()


def set_user_receive_marketing_email(email):
    qs = User.objects.filter(email__iexact=email)
    if qs.exists():
        user = User.objects.get(email__iexact=email)
        user.receive_marketing_email = True
        user.save()
        user.refresh_from_db()


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
