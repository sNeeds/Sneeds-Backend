from django.db.models.signals import post_save, pre_save
from django.core.signals import request_finished
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from abroadin.apps.users.customAuth.tasks import send_reset_password_email
from abroadin.settings.config.variables import FRONTEND_URL

from ..utils import user_creation_handle_contact, user_update_handle_contact

User = get_user_model()


def pre_save_user(sender, instance, *args, **kwargs):

    if instance._state.adding is True and instance._state.db is None:
        db_instance = None
    else:
        try:
            db_instance = User.objects.get(pk=instance.pk)
        except User.DoesNotExist:
            db_instance = None

    if db_instance is None:
        user_creation_handle_contact(instance)
    if db_instance is not None:
        user_update_handle_contact(instance, db_instance)


pre_save.connect(pre_save_user, sender=User, dispatch_uid="vjkvjbjvlbvl")


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.first_name,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            reverse('auth:password_reset:reset-password-request'),
            reset_password_token.key
        ),
        'token': reset_password_token.key,
    }
    reset_link = FRONTEND_URL + "auth/forget?token={}".format(context['token'])

    send_reset_password_email.delay(
        context['email'],
        context['current_user'].get_pretty_full_name(),
        reset_link,
    )
