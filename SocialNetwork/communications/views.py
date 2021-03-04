import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from dashboard.models import User
from friend.models import FriendRequest
from communications.models import Message
from rest_framework.authentication import SessionAuthentication
from . models import Room

from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from communications.serializers import MessageModelSerializer
# def all_messages(request):
#     friends_one = FriendRequest.objects.filter(receiver=request.user, status='friend')
#     friends_two = FriendRequest.objects.filter(sender=request.user, status='friend')
#     friends = friends_one | friends_two
    # room1 = Room.objects.all()
    # return render(request, "communications/all-messages.html", {'friend': friends})
    # return render(request, "communications/all-messages.html", {'room': room1})



# Conversation with one friend
class All_messages(TemplateView):
    model = FriendRequest
    template_name = "communications/all-messages.html"

    def get_context_data(self,**kwargs):
        friends_one = FriendRequest.objects.filter(receiver=self.request.user, status='friend')
        friends_two = FriendRequest.objects.filter(sender=self.request.user, status='friend')
        # friend_list = FriendRequest.objects.filter(receiver=self.request.user,status='friend')
        kwargs['friend_list'] = friends_one | friends_two
        # print(kwargs['friend_list'])
        return kwargs


# @login_required(login_url=reverse_lazy("dashboard:login"))
def messages_with_one_friend(request, friend):
    
    # print(friend)
    if request.user.username == friend:
        # print(friend)
        return redirect(reverse_lazy('communications:all-messages'))
    try:
        if not User.objects.get(username=friend):
            return redirect(reverse_lazy('communications:all-messages'))
    except:
        return redirect(reverse_lazy('communications:all-messages'))
    friends_one = FriendRequest.objects.filter(receiver=request.user, status='friend')
    # print(friends_one)
    friends_two = FriendRequest.objects.filter(sender=request.user, status='friend')
    # print(friends_two)
    friends = friends_one | friends_two
    # print(friends)
    return render(request, "communications/friend-messages.html", {
        'friends': friends,
        'friend_name_json': mark_safe(json.dumps(friend)),
        'username': mark_safe(json.dumps(request.user.username)),
    })
# 
class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return

class MessageModelViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageModelSerializer
     
    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(friend=request.user) |
                                             Q(author=request.user))
        target = self.request.query_params.get('target', None)
        print(target)
        if target is not None:
            self.queryset = self.queryset.filter(
                Q(friend=request.user, author__username=target) |
                Q(friend__username=target, author=request.user))
        return super(MessageModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(friend=request.user) |
                                 Q(author=request.user),
                                 Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        print(serializer)
        return Response(serializer.data)