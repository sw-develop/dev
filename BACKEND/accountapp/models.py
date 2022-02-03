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
    name = models.CharField(max_length=20, null=False)
    phone = models.CharField(max_length=20, null=False)
    gender = models.CharField(max_length=20, null=False)
    birthdate = models.DateField(null=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_user'

    def __str__(self):
        return f'(유저id:{self.user.id}, 이름:{self.name})'

    def check_mailbox_open_today(self):  # 오늘 오픈된 우체통이 있는지 체크
        for mailbox in self.mailboxes.all():
            if mailbox.open_date == date.today():
                return True
        return False

    def check_mailbox_today(self):  # 확인해야할 우체통이 있는지 체크
        # 오픈된 우체통이고 아직 사용자가 확인안했을 때
        for mailbox in self.mailboxes.all():
            if mailbox.open_date <= date.today() and mailbox.checked is False:
                return True
        return False

    def number_of_mailboxes(self):  # 우체통 개수 반환 메서드
        return self.mailboxes.count()

    def number_of_letters_in_unopened_mailbox(self):  # 오픈되지 않은 우체통에 담긴 편지 개수 반환 메서드
        total_letter = 0
        for mailbox in self.mailboxes.filter(
                open_date__gt=date.today()):  # SQL : SELECT ... WHERE open_date > date.today()
            total_letter += mailbox.number_of_letter()
        return total_letter
