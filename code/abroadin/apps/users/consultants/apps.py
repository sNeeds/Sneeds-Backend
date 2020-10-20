from django.apps import AppConfig


class ConsultantsConfig(AppConfig):
    name = 'abroadin.apps.users.consultants'

    def ready(self):
        import abroadin.apps.users.consultants.signals.handlers
