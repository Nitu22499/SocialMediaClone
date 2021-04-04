import json
from django.shortcuts import render, redirect
from dashboard.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.views.generic import ListView

from .serializers import NotificationSerializer
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class FindFriendsListView(LoginRequiredMixin, ListView):
    model = FriendRequest
    context_object_name = 'users'
    template_name = "friend/find-friends.html"
    
    def get_context_data(self, **kwargs):
        received_req = self.request.user.friends.values('sender')
        send_req = list(FriendRequest.objects.filter(sender=self.request.user,status='requested').values_list('receiver__username', flat=True))
        # print(send_req,received_req)

        friend_list_r = FriendRequest.objects.filter(receiver=self.request.user,status='friend')
        friend_list_s = FriendRequest.objects.filter(sender=self.request.user,status='friend')
        
        current_user_friends = (friend_list_r|friend_list_s).values('receiver')
    
        friend_list = friend_list_r|friend_list_s
        
        kwargs['friend_list']=friend_list

        sent_request = FriendRequest.objects.filter(sender=self.request.user,status='requested')
        kwargs['sent_request']=sent_request

        recieve_request = FriendRequest.objects.filter(receiver=self.request.user,status='requested')
        kwargs['recieve_request']=recieve_request

        users = User.objects.exclude(id=self.request.user.id).exclude(username__in=send_req).exclude(id__in=received_req).exclude(id__in=current_user_friends)
        kwargs['users']=users
        return kwargs
@login_required
def send_request(request, username=None):
    if username is not None:
        friend_user = User.objects.get(username=username)
        friend = FriendRequest.objects.create(sender=request.user, receiver=friend_user)
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

@login_required
def accept_request(request, friend=None):
    if friend is not None:
        friend_user = User.objects.get(username=friend)
        current_user = request.user
        f = FriendRequest.objects.filter(sender=friend_user, receiver=current_user, status='requested')[0]
        f.status = "friend"
        f.save()
        CustomNotification.objects.filter(recipient=current_user, actor=friend_user).delete()
        data = {
            'status': True,
            'message': "You accepted friend request",
        }
        return redirect('friend:find-friends')
