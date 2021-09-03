import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class SessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope["user"])
        # self.
        self.room_name = str(self.scope['url_route']['kwargs']['pk'])
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    
    async def chat_message(self, event):
        print("chat message")
        print(event)
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))