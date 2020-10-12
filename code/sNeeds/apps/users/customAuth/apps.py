from django.apps import AppConfig


class CustomAuthConfig(AppConfig):
    name = 'sNeeds.apps.users.customAuth'
    verbose_name = 'Auth'

    def ready(self):
        import sNeeds.apps.users.customAuth.signals.handlers
