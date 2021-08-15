from django.db import models
from django.utils import timezone
from mailboxapp.models import MailBox


class Letter(models.Model):
    target_mailbox = models.ForeignKey(MailBox, related_name='letter', on_delete=models.CASCADE)
    content = models.TextField(max_length=3000)
    sender = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    letter_created = models.DateTimeField(default=timezone.now)