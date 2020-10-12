from django.apps import AppConfig


class EstimationsConfig(AppConfig):
    name = 'sNeeds.apps.estimation.estimations'

    def ready(self):
        import sNeeds.apps.estimation.estimations.signals.handlers


