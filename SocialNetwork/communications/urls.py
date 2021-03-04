from django.urls import path,include
from .views import *

from rest_framework.routers import DefaultRouter
from communications.views import MessageModelViewSet

app_name = "communications"


router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')

urlpatterns = [
    path(r'api/v1/', include(router.urls)),

    path('', All_messages.as_view(), name="all-messages"),
    
    path('<slug:friend>', messages_with_one_friend, name="messages-with-one-friend"),
]
