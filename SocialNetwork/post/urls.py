from django.urls import path
from .views import *

app_name = "post"

urlpatterns = [
   
    # path('regiter', RegisterView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'),
    path('likes/', like_unlike_post, name='post_like'),
    path('comment/create/<int:post_id>', create_comment, name="comment-create"), 
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),       
]