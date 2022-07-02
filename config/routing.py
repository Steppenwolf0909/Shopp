from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chats.middleware import TokenAuthMiddlewareStack

from chats.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<str:uid>/', ChatConsumer.as_asgi()),
        ])
    ),
})