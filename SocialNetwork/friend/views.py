import json
from django.shortcuts import render, redirect
from dashboard.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.views.generic import ListView

from .serializers import NotificationSerializer
from .models import *


class FindFriendsListView(ListView):
    model = Friend
    context_object_name = 'users'
    template_name = "friend/find-friends.html"
    
    def get_context_data(self, **kwargs):
        current_user_friends = self.request.user.friends.values('id')
        sent_request = list(Friend.objects.filter(user=self.request.user,status='requested').values_list('friend_id__username', flat=True))
        kwargs['sent_request']=sent_request
        print(kwargs['sent_request'])
        users = User.objects.exclude(id__in=current_user_friends).exclude(username=sent_request).exclude(id=self.request.user.id)
        kwargs['users']=users
        print(kwargs['users'])
        recieve_request = Friend.objects.filter(friend=self.request.user,status='requested')
        kwargs['recieve_request']=recieve_request
        print(kwargs['recieve_request'])
        
        friend_list_r = Friend.objects.filter(friend=self.request.user,status='friend')
        friend_list_s = Friend.objects.filter(user=self.request.user,status='friend')
        kwargs['friend_list']=friend_list_r|friend_list_s
        print(kwargs['friend_list'])
        return kwargs

def send_request(request, username=None):
    if username is not None:
        friend_user = User.objects.get(username=username)
        friend = Friend.objects.create(user=request.user, friend=friend_user)
        notification = CustomNotification.objects.create(type="friend", recipient=friend_user, actor=request.user, verb="sent you friend request")
        channel_layer = get_channel_layer()
        channel = "notifications_{}".format(friend_user.username)
        async_to_sync(channel_layer.group_send)(
            channel, {
                "type": "notify",  # method name
                "command": "new_notification",
                "notification": json.dumps(NotificationSerializer(notification).data)
            }
        )
        data = {
            'status': True,
            'message': "Request sent.",
        }
        return redirect('friend:find-friends')
    else:
        pass


def accept_request(request, friend=None):
    if friend is not None:
        friend_user = User.objects.get(username=friend)
        current_user = request.user
        f = Friend.objects.filter(user=friend_user, friend=current_user, status='requested')[0]
        f.status = "friend"
        f.save()
        CustomNotification.objects.filter(recipient=current_user, actor=friend_user).delete()
        data = {
            'status': True,
            'message': "You accepted friend request",
        }
        return redirect('friend:find-friends')
