from datetime import date

from django.contrib.auth.models import User
from django.db import models


class AppUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='app_user'
    )  # user_id, related_name default : appuser
    name = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_user'

    def check_mailbox_open_today(self):  # 오늘 오픈된 우체통이 있는지 체크
        for mailbox in self.mailboxes.all():
            if mailbox.open_date == date.today():
                return True
        return False

    def number_of_mailboxes(self):  # 우체통 개수 반환 메서드
        return self.mailboxes.count()
