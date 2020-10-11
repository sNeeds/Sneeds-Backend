from django.apps import AppConfig


class BasicProductConfig(AppConfig):
    name = 'sNeeds.apps.store.basicProducts'

    def ready(self):
        import sNeeds.apps.store.basicProducts.signals.handlers
