import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from dashboard.models import User
from friend.models import Friend


def all_messages(request):
    friends_one = Friend.objects.filter(friend=request.user, status='friend')
    friends_two = Friend.objects.filter(user=request.user, status='friend')
    friends = friends_one | friends_two
    return render(request, "communications/all-messages.html", {'friend': friends})


# Conversation with one friend
class Friendslist(TemplateView):
    model = Friend
    template_name = "includes/sidebar"

    def get_context_data(self,**kwargs):
        friend_list = Friend.objects.filter(friend=self.request.user,status='friend')
        kwargs['friend_list']=friend_list
        return kwargs


@login_required(login_url=reverse_lazy("dashboard:login"))
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
    friends_one = Friend.objects.filter(friend=request.user, status='friend')
    print(friends_one)
    friends_two = Friend.objects.filter(user=request.user, status='friend')
    print(friends_two)
    friends = friends_one | friends_two
    print(friends)
    return render(request, "communications/friend-messages.html", {
        'friends': friends,
        'friend_name_json': mark_safe(json.dumps(friend)),
        'username': mark_safe(json.dumps(request.user.username)),
    })
