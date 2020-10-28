from django.apps import AppConfig


class AnalyzeConfig(AppConfig):
    name = 'abroadin.apps.estimation.analyze'

    def ready(self):
        import abroadin.apps.estimation.analyze.signals.handlers
