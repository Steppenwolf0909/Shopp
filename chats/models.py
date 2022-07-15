import uuid

from django.contrib.auth import get_user_model
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
User = get_user_model()



class Message(models.Model):
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='messages',
        verbose_name='Автор'
    )
    text = models.TextField(blank=True, null=True, verbose_name='Текст')
    chat = models.ForeignKey(
        'Chat', on_delete=models.CASCADE, related_name='chat_messages',
        verbose_name='Чат'
    )
    is_read = models.BooleanField(default=False)
    uid = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created_at',
    )
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name='modified_at',
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['created_at']

    @property
    def file_size(self):
        return self.file.size if self.file else None

    def __str__(self):
        return f'{self.__class__.__name__}: {str(self.uid)}'


class Chat(models.Model):
    first_client = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True,
        related_name='first_client', verbose_name='Первый клиент'
    )
    second_client = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True,
        related_name='second_client', verbose_name='Второй клиент'
    )
    uid = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created_at',
    )
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name='modified_at',
    )

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['created_at']

    @property
    def get_last_message(self):
        return self.chat_messages.last()

    def __str__(self):
        return f'{self.__class__.__name__}: {str(self.uid)}'




@receiver(post_save, sender=User)
def create_favorites(sender, instance, created, **kwargs):
    if (created) & (instance.email!='supportmail@mail.com'):
        support = User.objects.filter(id=1).first()
        chat = Chat(
            first_client = instance,
            second_client = support
        )
        Chat.save(chat)