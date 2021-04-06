from django.urls import path
from .views import *

app_name = "dashboard"

urlpatterns = [
   
    path('register', RegisterView.as_view(), name='register'),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name = 'logout'),
    path('profile/', ProfileView.as_view(), name = 'profile'),
    path('profile/<slug:pk>', profile_view, name = 'profile_view'),
    path('edit_profile/',Edit_Profile.as_view(), name='edit_profile'),
    path('upload-profile-pic/', UploadProfilePic.as_view(), name = 'uploadprofile'),
    path('search/', searchUser, name = 'search'),
    path('ajax-search/', ajax_search, name = 'ajax-search'),
    # path('ajax-search/', autocompleteModel, name = 'ajax-search'),
    


]