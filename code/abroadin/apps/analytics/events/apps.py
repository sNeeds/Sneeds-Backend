import posthog

from django.apps import AppConfig
from abroadin.settings.secure.APIs import posthog as posthog_api


class EventConfig(AppConfig):
    name = 'abroadin.apps.analytics.events'

    def ready(self):
        posthog.api_key = posthog_api
        posthog.host = 'https://app.posthog.com'

        posthog.capture('test-id', 'test-event')

