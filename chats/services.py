import logging

from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

from .models import Chat, Message
# from clients.models import User

logger = logging.getLogger(__name__)

User = get_user_model()


class ChatService:

    @classmethod
    @database_sync_to_async
    def get_chat(cls, chat_id, user):
        if not user.is_authenticated:
            raise DenyConnection()
        try:
            chat = Chat.objects.get(uid=chat_id)
        except Chat.DoesNotExist:
            raise DenyConnection()
        return chat

    @classmethod
    @database_sync_to_async
    def get_message_author(cls, message):
        return message.author

    @classmethod
    @database_sync_to_async
    def create_message(cls, message_data):
        message_data["author"] = message_data["author"]
        return Message.objects.create(
            **message_data
        )

    @classmethod
    @database_sync_to_async
    def read_message(cls, message_uid):
        try:
            message = Message.objects.get(uid=message_uid)
            message.is_read = True
            message.save(update_fields=['is_read'])
            return message
        except Message.DoesNotExist:
            return None

    @classmethod
    async def message_to_json(cls, message):
        data = {
            'uid': f'{message.uid}',
            'author': f'{message.author}',
            'text': f'{message.text}',
            'created_at': f'{message.created_at}',
            'is_read': message.is_read,
            'user_id': await cls.get_user(message)
        }
        return data

    @classmethod
    @database_sync_to_async
    def get_user(cls, message):
        user_id = User.objects.filter(id=message.author.id)
        if user_id:
            return user_id.first().id
        return None