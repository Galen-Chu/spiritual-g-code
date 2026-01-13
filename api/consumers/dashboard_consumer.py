"""
WebSocket consumers for Spiritual G-Code.
Handles real-time dashboard updates.
"""

import json
import logging
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class DashboardConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for dashboard real-time updates.

    Features:
    - Real-time G-Code score updates
    - Automatic reconnection support
    - User-specific channel subscription
    """

    async def connect(self):
        """
        Accept WebSocket connection and subscribe to user's channel.
        Authentication is handled by AuthMiddlewareStack in asgi.py.
        """
        try:
            # Get user from scope (populated by AuthMiddlewareStack)
            self.user = self.scope["user"]

            if self.user.is_anonymous:
                logger.warning("WebSocket connection rejected: Anonymous user")
                await self.close()
                return

            # Create user-specific channel name
            self.user_group_name = f'dashboard_{self.user.id}'

            # Join user's channel group
            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
            )

            await self.accept()

            logger.info(f"WebSocket connected for user {self.user.id}")

            # Send connection confirmation
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'user_id': self.user.id,
                'message': 'WebSocket connection established'
            }))

        except Exception as e:
            logger.error(f"WebSocket connection error: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.
        Leave the user's channel group.
        """
        try:
            if hasattr(self, 'user_group_name'):
                await self.channel_layer.group_discard(
                    self.user_group_name,
                    self.channel_name
                )
                logger.info(f"WebSocket disconnected for user {self.user.id if hasattr(self, 'user') else 'unknown'}")
        except Exception as e:
            logger.error(f"WebSocket disconnect error: {str(e)}")

    async def receive(self, text_data):
        """
        Handle incoming messages from WebSocket client.

        Client can send:
        - ping: Keep-alive message
        - subscribe: Subscribe to specific updates
        - unsubscribe: Unsubscribe from updates
        """
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'ping':
                # Respond with pong
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': str(timezone.now())
                }))

            elif message_type == 'subscribe':
                # Handle subscription to specific update types
                await self.send(text_data=json.dumps({
                    'type': 'subscription_confirmed',
                    'updates': data.get('updates', [])
                }))

            else:
                logger.warning(f"Unknown message type: {message_type}")

        except json.JSONDecodeError:
            logger.error("Invalid JSON received from WebSocket")
        except Exception as e:
            logger.error(f"Error receiving WebSocket message: {str(e)}")

    async def dashboard_update(self, event):
        """
        Handle dashboard update events from channel layer.

        Event structure:
        {
            'type': 'gcode_update',
            'data': {...}
        }
        """
        try:
            # Send update to client
            await self.send(text_data=json.dumps({
                'type': event.get('type'),
                'data': event.get('data')
            }))

        except Exception as e:
            logger.error(f"Error sending dashboard update: {str(e)}")
