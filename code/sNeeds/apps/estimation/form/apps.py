from django.apps import AppConfig


class EstimationFormConfig(AppConfig):
    name = 'sNeeds.apps.estimation.form'

    def ready(self):
        import sNeeds.apps.estimation.form.signals.handlers


