from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from communications import routing as communications_routing
from ChatMessage import routing as ChatMessage_routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns + communications_routing.websocket_urlpatterns + ChatMessage_routing.websocket_urlpatterns
        )
    ),
})