import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from dashboard.models import User
from friend.models import FriendRequest
from . models import Room


def all_messages(request):
    friends_one = FriendRequest.objects.filter(receiver=request.user, status='friend')
    friends_two = FriendRequest.objects.filter(sender=request.user, status='friend')
    friends = friends_one | friends_two
    # room1 = Room.objects.all()
    return render(request, "communications/all-messages.html", {'friend': friends})
    # return render(request, "communications/all-messages.html", {'room': room1})



# Conversation with one friend
class All_messages(TemplateView):
    model = FriendRequest
    template_name = "communications/all-messages.html"

    def get_context_data(self,**kwargs):
        
        friend_list = FriendRequest.objects.filter(receiver=self.request.user,status='friend')
        kwargs['friend_list']=friend_list
        return kwargs


# @login_required(login_url=reverse_lazy("dashboard:login"))
def messages_with_one_friend(request, friend):
    
    print(friend)
    if request.user.username == friend:
        print(friend)
        return redirect(reverse_lazy('communications:all-messages'))
    try:
        if not User.objects.get(username=friend):
            return redirect(reverse_lazy('communications:all-messages'))
    except:
        return redirect(reverse_lazy('communications:all-messages'))
    friends_one = FriendRequest.objects.filter(receiver=request.user, status='friend')
    print(friends_one)
    friends_two = FriendRequest.objects.filter(sender=request.user, status='friend')
    print(friends_two)
    friends = friends_one | friends_two
    print(friends)
    return render(request, "communications/friend-messages.html", {
        'friends': friends,
        'friend_name_json': mark_safe(json.dumps(friend)),
        'username': mark_safe(json.dumps(request.user.username)),
    })
# 