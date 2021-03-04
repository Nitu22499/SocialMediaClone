from ChatMessage.consumers import ChatMessageConsumer

from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^ws$', ChatMessageConsumer),
]