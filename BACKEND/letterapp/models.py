from django.db import models

from mailboxapp.models import MailBox


class Letter(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='letter_id')
    mailbox = models.ForeignKey(MailBox, on_delete=models.CASCADE, related_name='letters')
    content = models.TextField()
    sender = models.CharField(max_length=20)
    receiver = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    checked = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'letter'

    def __str__(self):
        return f'{self.mailbox} -> (편지id:{self.id}, 편지내용:{self.content[:10]})'
