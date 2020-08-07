from django.apps import AppConfig


class EstimationsConfig(AppConfig):
    name = 'sNeeds.apps.estimations'

    def ready(self):
        import sNeeds.apps.estimations.signals.handlers
