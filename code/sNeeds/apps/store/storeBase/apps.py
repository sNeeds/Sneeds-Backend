from django.apps import AppConfig


class StoreConfig(AppConfig):
    name = 'sNeeds.apps.store.storeBase'

    def ready(self):
        import sNeeds.apps.store.storeBase.signals.handlers
