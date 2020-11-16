from django.contrib import admin
from friend.models import FriendRequest,CustomNotification
# Register your models here.
admin.site.register(FriendRequest)
admin.site.register(CustomNotification)