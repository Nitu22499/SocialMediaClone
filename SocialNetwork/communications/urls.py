from django.urls import path,include
from .views import *


app_name = "communications"



urlpatterns = [
    path('', All_messages.as_view(), name="all-messages"),
    path('<slug:friend>', messages_with_one_friend, name="messages-with-one-friend"),
]
