from django.core.mail import EmailMessage
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
import datetime
from mailboxapp.models import MailBox

from BACKEND.settings.local import TEAM_PW  # local mode
# from BACKEND.settings.deploy import TEAM_PW  # deploy mode


def send_email_to_admin(phones, unchecked_mailboxes, to):
    # title
    title = '아직 처리되지 않은 메일박스 목록 보내드립니다.'

    # msg
    msg = []
    msg.append('\n'.join(map(str, phones)))
    msg.append("\n\n유저들에게 카톡 메세지 전송 후, admin 페이지에서 아래의 Mailbox ID를 check 표시 해주세요")
    msg.append('\n'.join(map(str, unchecked_mailboxes)))

    # send
    mail = EmailMessage(title, '\n'.join(msg), to=[to])
    mail.send()


class MailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'adminapp/base.html', {})

    def post(self, request):
        to = request.data['email']
        pw = request.data['pw']

        if pw == TEAM_PW:
            # filter 기준 1. checked 되지 않음
            # filter 기준 2. 공개날짜가 today이거나 그 이전인 mailbox여야함
            # filter 기준 3. mailbox가 가지고 있는 편지의 개수가 1개 이상이어야 함
            # => mailbox들에 해당하는 유저의 phone 번호, mailbox id 가져옴
            mailbox_objs = MailBox.objects.filter(checked=False)
            mailbox_objs = mailbox_objs.filter(open_date__lte=datetime.datetime.today()).order_by('id')
            mailbox_objs = [obj for obj in mailbox_objs if obj.number_of_letter() >= 1]

            if len(mailbox_objs) == 0:
                response_msg = "처리할 메일박스가 없습니다!"
                return HttpResponse(response_msg, status=200)

            unchecked_usrs = [obj.user for obj in mailbox_objs]
            phones = [unchk_usr.phone for unchk_usr in unchecked_usrs]
            unchecked_mailboxes = [obj.id for obj in mailbox_objs]

            send_email_to_admin(phones, unchecked_mailboxes, to)

            # make a response msg
            now = datetime.datetime.now()
            now_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
            response_msg = to + " 로 " + str(len(unchecked_mailboxes)) + "개 목록 전송되었습니다 - " + now_datetime

            return HttpResponse(response_msg, status=200)

        else:
            response_msg = "우리 팀이 아니시군요?"
            return HttpResponse(response_msg, status=200)
