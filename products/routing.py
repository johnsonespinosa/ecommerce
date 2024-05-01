from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from products import consumers

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': URLRouter([
        path('ws/stock/', consumers.StockConsumer.as_asgi()),
    ]),
})

application = AuthMiddlewareStack(application)