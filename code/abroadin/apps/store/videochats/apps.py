from django.apps import AppConfig


class VideoChatsConfig(AppConfig):
    name = 'abroadin.apps.store.videochats'

    def ready(self):
        import abroadin.apps.store.videochats.signals.handlers
