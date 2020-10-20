from django.apps import AppConfig


class CustomAuthConfig(AppConfig):
    name = 'abroadin.apps.users.customAuth'
    verbose_name = 'Auth'

    def ready(self):
        import abroadin.apps.users.customAuth.signals.handlers
