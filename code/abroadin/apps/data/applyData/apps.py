from django.apps import AppConfig


class ApplydataConfig(AppConfig):
    name = 'abroadin.apps.data.applyData'

    def ready(self):
        from .signals import handlers
