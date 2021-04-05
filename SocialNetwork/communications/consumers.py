import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


from communications.models import Message
from dashboard.models import User

class CommunicationConsumer(AsyncWebsocketConsumer):
    async def connect(self):       
        self.room_name = self.scope['url_route']['kwargs']['friend']
        self.room_group_name = 'communications_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print("dis")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @sync_to_async
    def get_author(self,user):
        return User.objects.get(username=user)
    
    @sync_to_async
    def get_friend(self,friend):
        return User.objects.get(username=friend)
    
    @sync_to_async
    def create_messages(self,author,friend,message):
        return Message.objects.create(author=author,friend=friend,message=message)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = await self.get_author(text_data_json['author'])
        print(user)
        friend = await self.get_friend(text_data_json['friend'])
        messages = await self.create_messages(user, friend, text_data_json['message'])
        timestamp = str(messages.timestamp)
        message = text_data_json['message']
        author = text_data_json['author']
        friend = text_data_json['friend']
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'author': author,
                'friend':friend,
                'message': message,
                'timestamp':timestamp
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        author = event['author']
        friend = event['friend']
        message = event['message']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
                'author': author,
                'friend':friend,
                'message': message,
                'timestamp':timestamp
        }))