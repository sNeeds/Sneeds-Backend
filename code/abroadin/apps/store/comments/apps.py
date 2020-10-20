from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = 'abroadin.apps.store.comments'
    verbose_name = 'Comment'

    def ready(self):
        import abroadin.apps.store.comments.signals.handlers
