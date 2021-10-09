from django.core.mail import EmailMessage
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
import datetime
from mailboxapp.models import MailBox

# from BACKEND.settings.local import TEAM_PW  # local mode
from BACKEND.settings.deploy import TEAM_PW  # deploy mode


def send_email_to_admin(phones, unchecked_mailboxes, to):
    # title
    title = '아직 처리되지 않은 메일박스 목록 보내드립니다.'

    # msg
    msgs = []
    return 0
    # msgs.append('\n'.join(phones))
    # msgs.append("\n\n유저들에게 카톡 메세지 전송 후, admin 페이지에서 아래의 Mailbox ID를 check 표시 해주세요")
    # msgs.append('\n'.join(map(str, unchecked_mailboxes)))
    # email_msg = '\n'.join(msgs)


    # send
    # mail = EmailMessage(title, email_msg, to=[to])
    # mail.send()


class MailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'adminapp/base.html', {})

    def post(self, request):
        to = request.data['email']
        pw = request.data['pw']

        if pw == TEAM_PW:
            # 체크 안된 mailbox들 찾아서 phone 번호, mailbox id 가져옴
            mailbox_objs = MailBox.objects.filter(checked=False).order_by('id')

            if len(mailbox_objs) == 0:
                response_msg = "처리할 메일박스가 없습니다!"
                return HttpResponse(response_msg, status=200)

            unchecked_usrs = [obj.user for obj in mailbox_objs]
            phones = [unchk_usr.phone for unchk_usr in unchecked_usrs]
            unchecked_mailboxes = [obj.id for obj in mailbox_objs]

            dum = send_email_to_admin(phones, unchecked_mailboxes, to)
            print(dum)

            # make a response msg
            now = datetime.datetime.now()
            now_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
            response_msg = to + " 로 " + str(len(unchecked_mailboxes)) + "개 목록 전송되었습니다 - " + now_datetime

            return HttpResponse(response_msg, status=200)

        else:
            response_msg = "우리 팀이 아니시군요?"
            return HttpResponse(response_msg, status=200)
