from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = 'sNeeds.apps.store.comments'
    verbose_name = 'Comment'

    def ready(self):
        pass
