from django.apps import AppConfig


class ChatsConfig(AppConfig):
    name = 'abroadin.apps.chats'

    def ready(self):
        import abroadin.apps.chats.signals.handlers
