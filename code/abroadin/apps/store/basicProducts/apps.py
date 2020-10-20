from django.apps import AppConfig


class BasicProductConfig(AppConfig):
    name = 'abroadin.apps.store.basicProducts'

    def ready(self):
        import abroadin.apps.store.basicProducts.signals.handlers
