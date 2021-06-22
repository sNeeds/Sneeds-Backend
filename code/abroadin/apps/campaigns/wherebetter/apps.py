from django.apps import AppConfig


class WhereBetterCampaignConfig(AppConfig):
    name = 'abroadin.apps.campaigns.wherebetter'

    def ready(self):
        from .signals import handlers
