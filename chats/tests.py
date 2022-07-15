from django.test import TestCase
from clients.models import User
from .models import Chat

class ViewTest(TestCase):

    def test_creating_chat_after_user(self):
        User.objects.create(email='supportmail@mail.com')
        User.objects.create(email='testmail@mail.com')
        chat = Chat.objects.all().first()
        self.assertEqual(chat.first_client.email, 'testmail@mail.com')


