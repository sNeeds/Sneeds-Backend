from django.apps import AppConfig


class EstimationsConfig(AppConfig):
    name = 'abroadin.apps.estimation.estimations'

    def ready(self):
        import abroadin.apps.estimation.estimations.signals.handlers


