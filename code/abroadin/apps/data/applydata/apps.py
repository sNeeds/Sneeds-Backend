from django.apps import AppConfig


class ApplydataConfig(AppConfig):
    name = 'abroadin.apps.data.applydata'

    def ready(self):
        from .signals import handlers
