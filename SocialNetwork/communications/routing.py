from django.conf.urls import url

from communications.consumers import CommunicationConsumer

websocket_urlpatterns = [
   url(r'^ws/communications/(?P<friend>[^/]+)/$', CommunicationConsumer),
]