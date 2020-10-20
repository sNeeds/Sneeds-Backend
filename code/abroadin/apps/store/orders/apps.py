from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'abroadin.apps.store.orders'

    def ready(self):
        import abroadin.apps.store.orders.signals.handlers
