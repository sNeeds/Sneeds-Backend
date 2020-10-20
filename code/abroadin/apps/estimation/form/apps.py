from django.apps import AppConfig


class EstimationFormConfig(AppConfig):
    name = 'abroadin.apps.estimation.form'

    def ready(self):
        import abroadin.apps.estimation.form.signals.handlers


