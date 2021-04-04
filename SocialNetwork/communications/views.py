import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from dashboard.models import User
from friend.models import FriendRequest
from communications.models import Message


class All_messages(TemplateView):
    model = FriendRequest
    template_name = "communications/all-messages.html"

    def get_context_data(self,**kwargs):
        friend_list_r = FriendRequest.objects.filter(receiver=self.request.user,status='friend')
        friend_list_s = FriendRequest.objects.filter(sender=self.request.user,status='friend')
       
        friend_list = friend_list_r|friend_list_s
        for friend in friend_list :
            if friend.sender.id == self.request.user.id :
                print(friend.receiver.username)
            else:
                print(friend.sender.username)

        kwargs['friend_list']=friend_list
        print(kwargs['friend_list'])
        return kwargs


# @login_required(login_url=reverse_lazy("dashboard:login"))
def messages_with_one_friend(request, friend):
    if request.user.username == friend:
        return redirect(reverse_lazy('communications:all-messages'))
    try:
        if not User.objects.get(username=friend):
            return redirect(reverse_lazy('communications:all-messages'))
    except:
        return redirect(reverse_lazy('communications:all-messages'))

    friends_one = FriendRequest.objects.filter(receiver=request.user, status='friend')
    friends_two = FriendRequest.objects.filter(sender=request.user, status='friend')
    friends = friends_one | friends_two
   
    friend_url=None
    user_url=None
    frnd = friends.filter(sender__username=friend)
    if frnd:
        friend_url = frnd[0].sender.user_image.url

    usr = friends.filter(receiver__username=friend)
    if usr:
        user_url = usr[0].receiver.user_image.url
    print(user_url,friend_url)
    
    chat_r = Message.objects.filter(friend__username=request.user.username, author__username=friend)
    print(request.user.username,friend,chat_r)
    chat_s = Message.objects.filter(friend__username=friend, author__username=request.user.username)
    print(chat_s)
    chat = (chat_r | chat_s).order_by('timestamp')
    print(chat)
    return render(request, "communications/friend-messages.html", {
        'chat':chat,
        'friends': friends,
        'friend_image_json':mark_safe(json.dumps(str(friend_url))),
        'user_image_json':mark_safe(json.dumps(str(user_url))),
        'friend_name_json': mark_safe(json.dumps(friend)),
        'username': mark_safe(json.dumps(request.user.username)),
    })

