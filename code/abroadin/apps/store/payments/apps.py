from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    name = 'abroadin.apps.store.payments'

    def ready(self):
        import abroadin.apps.store.payments.signals.handlers
