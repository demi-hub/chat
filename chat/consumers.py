from datetime import datetime
import logging
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from chat.models import User, ChatHistory

logger = logging.getLogger( __name__ )

class Chat(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'group_chat_{self.room_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print("channel connected successfully")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("channel disconnected")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room_id = text_data_json['room_id']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']

        await self.save_message(room_id, sender, receiver, message)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender':sender,
                'receiver':receiver,
                'message': message,
                'room_id': room_id
            }
        )
    
    async def chat_message(self, event):
        try:
            message = event['message']
            sender = event['sender']
            receiver = event['receiver']
            room_id = event['room_id']
            
            # time = await self.get_time_val(room_id)
            user = await sync_to_async(User.objects.get)(id=sender)
            await self.send(text_data=json.dumps({
                    'sender':user.first_name,
                    'sender_id':sender,
                    'receiver':receiver,
                    'message':message,
                    'room_id':room_id,
                    # 'created_on':time
                    'notification': f"New message from {user.first_name}"
                }))
        except Exception as e:
            logger.error(f"{str(e)}:",exc_info=True)    
        
        
        # user = ChatHistory.objects.get(sender=sender)
        # await self.send(text_data=json.dumps({
        #     'sender':sender,
        #     'receiver':receiver,
        #     'message': message,
        #     'notification': f"New message from {sender}"
        # }))

    @sync_to_async
    def save_message(self,room_id,sender,receiver,message):
        sender_= User.objects.get(id=sender)
        receiver_= User.objects.get(id=receiver)
        history_save=ChatHistory(room_id=room_id, sender=sender_, receiver=receiver_, message=message, updated_on=datetime.now())
        history_save.save()
        
