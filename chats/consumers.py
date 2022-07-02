import json
import logging

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chats.services import ChatService

logger = logging.getLogger(__name__)

chat_service = ChatService


class ChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.chat = None
        self.room_name = ''
        self.room_group_name = ''

    async def new_message(self, data):
        message = await chat_service.create_message({
            'author': self.user,
            'chat': self.chat,
            'text': data.get('text'),
        })
        await self.send_chat_message(
            message=await chat_service.message_to_json(message)
        )

    async def read_message(self, data):
        message_uid = data.get('message_uid')
        message = await chat_service.read_message(message_uid)
        if not message:
            await self.error_response(f'Message {message_uid} not found')
        else:
            await self.send_chat_message(
                message=await chat_service.message_to_json(message)
            )

    commands = {
        'new_message': new_message,
        'message_read': read_message,
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['uid']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']
        self.chat = await chat_service.get_chat(
            chat_id=self.room_name,
            user=self.user,
        )

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        # await self.send_json({
        #     'message': f'User {self.user.id} connected!'
        # })

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get('command')
        if command not in self.commands or not command:
            await self.error_response(f'Command {command} not valid')
        await self.commands[command](self, data)

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def error_response(self, message):
        await self.send_json(dict(
            message=message
        ))
        await self.close()

    async def send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
