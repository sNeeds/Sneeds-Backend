from django.apps import AppConfig


class ConsultantsConfig(AppConfig):
    name = 'sNeeds.apps.users.consultants'

    def ready(self):
        import sNeeds.apps.users.consultants.signals.handlers
