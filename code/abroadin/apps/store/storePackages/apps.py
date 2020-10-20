from django.apps import AppConfig


class StorePackagesConfig(AppConfig):
    name = 'abroadin.apps.store.storePackages'

    def ready(self):
        import abroadin.apps.store.storePackages.signals.handlers
