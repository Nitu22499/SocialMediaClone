from dashboard.models import User
from django.shortcuts import get_object_or_404
from communications.models import Message
from rest_framework.serializers import ModelSerializer, CharField


class MessageModelSerializer(ModelSerializer):
    # author = CharField(source='author.username', read_only=True)
    # friend = CharField(source='friend.username')

    def create(self, validated_data):
        # print(request.data)
        author = self.context['request'].user
        print("auth",author)
        friend = get_object_or_404(User, username=validated_data['friend'])
        print("fr",friend)
        msg = Message(friend=friend,
                           message=validated_data['message'],
                           author=author)
        print("m",msg)
        msg.save()
        return msg

    class Meta:
        model = Message
        fields = ('id', 'author', 'friend', 'timestamp', 'message')

