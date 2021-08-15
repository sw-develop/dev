from django.db import models
from django.utils import timezone
from accountapp.models import AppUser


class MailBox(models.Model):
    usr = models.ForeignKey(AppUser, related_name='MailBox', on_delete=models.CASCADE)
    mailbox_name = models.CharField(max_length=40)
    user_nickname = models.CharField(max_length=20)
    mailbox_url = models.URLField()
    theme = models.CharField(max_length=20)
    mailbox_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)
    open_date = models.DateTimeField(default=timezone.now)
