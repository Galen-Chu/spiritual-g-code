"""
WebSocket URL routing for Spiritual G-Code.
Defines all WebSocket URL patterns.
"""

from django.urls import re_path
from api.consumers import DashboardConsumer

websocket_urlpatterns = [
    re_path(r'^ws/dashboard/$', DashboardConsumer.as_asgi()),
]
