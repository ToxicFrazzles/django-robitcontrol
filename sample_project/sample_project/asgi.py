import os
from django.core.asgi import get_asgi_application

http_app = get_asgi_application()

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from . import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blokegaming.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": http_app,      # HTTP protocol request handler
    "websocket": AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
})
