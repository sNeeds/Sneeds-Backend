from django.apps import AppConfig


class CartsConfig(AppConfig):
    name = 'sNeeds.apps.store.carts'

    def ready(self):
        import sNeeds.apps.store.carts.signals.handlers