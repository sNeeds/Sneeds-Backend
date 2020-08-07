from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'sNeeds.apps.account'

    def ready(self):
        import sNeeds.apps.account.signals.handlers
