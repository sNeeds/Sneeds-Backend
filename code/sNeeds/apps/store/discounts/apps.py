from django.apps import AppConfig


class DiscountsConfig(AppConfig):
    name = 'sNeeds.apps.store.discounts'

    def ready(self):
        import sNeeds.apps.store.discounts.signals.handlers
