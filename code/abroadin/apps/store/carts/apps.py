from django.apps import AppConfig


class CartsConfig(AppConfig):
    name = 'abroadin.apps.store.carts'

    def ready(self):
        import abroadin.apps.store.carts.signals.handlers