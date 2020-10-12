from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    name = 'sNeeds.apps.store.payments'

    def ready(self):
        import sNeeds.apps.store.payments.signals.handlers
