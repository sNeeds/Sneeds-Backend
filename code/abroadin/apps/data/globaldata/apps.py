from django.apps import AppConfig


class GlobalDataConfig(AppConfig):
    name = 'abroadin.apps.data.globaldata'

    def ready(self):
        pass
