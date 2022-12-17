from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from users.models import Marketer


class Chat(models.Model):
    # members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Members")
    chat_support = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="chats",
        on_delete=models.PROTECT,
        null=True,
        blank=False,
    )
    chat_marketer = models.OneToOneField(Marketer, null=True, on_delete=models.SET_NULL)

    # def get_absolute_url(self):
    #     return reverse('chat:messages', kwargs={'chat_id': self.pk})


class Message(models.Model):
    chat = models.ForeignKey(
        Chat, related_name="chat_messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_messages",
        null=True,
        on_delete=models.SET_NULL,
    )
    message_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    new = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.message_text
