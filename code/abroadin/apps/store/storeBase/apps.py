from django.apps import AppConfig


class StoreConfig(AppConfig):
    name = 'abroadin.apps.store.storeBase'

    def ready(self):
        import abroadin.apps.store.storeBase.signals.handlers
