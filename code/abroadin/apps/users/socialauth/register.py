from celery import shared_task
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from abroadin.utils.pakat_mail_services import send_email

User = get_user_model()


def _register_user(*args, **kwargs):
    user = User.objects.create_user(**kwargs)
    user.is_verified = True
    user.is_email_verified = True
    user.set_unusable_password()
    user.save()
    return user


def get_jwt_tokens(user):
    data = {}
    refresh = RefreshToken.for_user(user)

    data['refresh'] = str(refresh)
    data['access'] = str(refresh.access_token)

    return data


@shared_task()
def send_webinar_discount(*args, **kwargs):
    send_email(send_to=kwargs.pop('send_to'), mail_template=kwargs.pop('mail_template'), **kwargs)


def login_register_social_user(email, provider, first_name, last_name):
    assert provider in User.AuthProviderTypeChoices.values

    filtered_user = User.objects.filter(email=email)
    user_exists = filtered_user.exists()

    if user_exists:
        user = filtered_user[0]
        user.auth_provider = provider
        user.is_verified = True
        user.is_email_verified = True
        user.save()
    else:
        user = _register_user(
            email=email, first_name=first_name, last_name=last_name,
            auth_provider=provider
        )
        send_webinar_discount.delay(send_to=user.email, mail_template=121)

    return user
