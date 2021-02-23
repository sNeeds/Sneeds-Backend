import datetime

from django.contrib.auth import get_user_model


def student_info_year_choicess():
    return [(r, r) for r in range(2000, datetime.date.today().year + 4)]


def student_info_year_choices():
    return [r for r in range(2000, datetime.date.today().year + 4)]


def get_users_interact_with_consultant_by_chat(consultant_profile):
    from abroadin.apps.chats.models import Chat
    return Chat.objects.filter(consultant=consultant_profile).get_users()


def add_this_arg(func):
    def wrapped(*args, **kwargs):
        return func(wrapped, *args, **kwargs)
    return wrapped
