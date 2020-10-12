from django.apps import AppConfig


class StorePackagesConfig(AppConfig):
    name = 'sNeeds.apps.store.storePackages'

    def ready(self):
        import sNeeds.apps.store.storePackages.signals.handlers
