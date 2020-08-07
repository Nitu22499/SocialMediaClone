from django.urls import path
from .views import *

app_name = "post"

urlpatterns = [
   
    # path('regiter', RegisterView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'),
    path('comment/create/<int:post_id>', create_comment, name="comment-create"),        
]