from django.apps import AppConfig


class VideoChatsConfig(AppConfig):
    name = 'sNeeds.apps.store.videochats'

    def ready(self):
        import sNeeds.apps.store.videochats.signals.handlers
