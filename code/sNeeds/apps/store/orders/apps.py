from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'sNeeds.apps.store.orders'

    def ready(self):
        import sNeeds.apps.store.orders.signals.handlers
