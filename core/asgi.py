"""
ASGI config for Spiritual G-Code project.
Supports both HTTP and WebSocket protocols.
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# Import WebSocket routing
import core.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

# ProtocolTypeRouter routes HTTP and WebSocket traffic
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            core.routing.websocket_urlpatterns
        )
    ),
})
