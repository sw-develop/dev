from rest_framework import serializers
from mailboxapp.models import MailBox


# 우체통 생성
class CreateMailBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailBox
        fields = ['nickname']


def get_number_of_letter(obj):
    return obj.number_of_letter()


# 개인 우체통 조회 - mailbox_id, link_title, mailbox_link, open_date & 편지 개수
class ListMailBoxSerializer(serializers.ModelSerializer):
    number_of_letter = serializers.SerializerMethodField()

    class Meta:
        model = MailBox
        fields = ['id', 'link_title', 'mailbox_link', 'open_date', 'number_of_letter']
