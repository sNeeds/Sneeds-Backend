import os

# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from abroadin.settings.middlewares.middlewares import AuthMiddlewareStack

DEPLOYMENT = int(os.environ.get('DJANGO_DEPLOYMENT', default=0))

if DEPLOYMENT == 1:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abroadin.settings.deployment')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abroadin.settings.development')


from abroadin.apps.campaigns.wherebetter import routing as wherebetter_routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            wherebetter_routing.websocket_urlpatterns
        )
    ),
})