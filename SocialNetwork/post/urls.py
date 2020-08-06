from django.urls import path
from .views import *

app_name = "post"

urlpatterns = [
   
    # path('regiter', RegisterView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'),

]