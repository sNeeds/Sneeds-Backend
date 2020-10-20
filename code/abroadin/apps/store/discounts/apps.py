from django.apps import AppConfig


class DiscountsConfig(AppConfig):
    name = 'abroadin.apps.store.discounts'

    def ready(self):
        import abroadin.apps.store.discounts.signals.handlers
