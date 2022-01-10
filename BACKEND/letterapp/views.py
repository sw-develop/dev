from datetime import datetime, timedelta
from json import dumps
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from letterapp.models import Letter
from mailboxapp.models import MailBox
from .serializers import CreateLetterSerializer


class LetterRequestView(APIView):
    permission_classes = [AllowAny]

    # url에 적힌 key로 메일박스에서 해당 mailbox pk 있는지 뒤져서
    # 있으면 -> ok, 없으면 -> no such mailbox in DB
    def get(self, request, mailbox_pk, random_strkey):
        try:
            mailbox_obj = MailBox.objects.get(id=mailbox_pk, key=random_strkey)

            # 우체통 동봉된 이후에 유저의 접근!!
            if datetime.now() > mailbox_obj.date_created + timedelta(hours=72):  # 배포용 : hours=72, 테스트용 : hours=24
                return HttpResponse(
                    "No! User accesses after mailbox has been enclosed",
                    status=400
                )

            # ok response
            RESPONSE_DATA = dict()
            RESPONSE_DATA['mailbox_pk'] = mailbox_obj.id
            RESPONSE_DATA['nickname'] = mailbox_obj.nickname
            return HttpResponse(
                dumps(RESPONSE_DATA, indent=4),
                content_type=u"application/json; charset=utf-8",
                status=200
            )

        # 유저가 잘못된 url을 입력하여 접근 (url에 적힌 random_strkey가 DB에 없음)
        except MailBox.DoesNotExist:
            return HttpResponse(
                "No! The requested mailbox not exists in DB",
                status=400
            )

    def post(self, request, mailbox_pk, random_strkey):
        try:
            mailbox_obj = MailBox.objects.get(id=mailbox_pk, key=random_strkey)

            # ok response
            serializer = CreateLetterSerializer(data=request.data)  # CreateLetterSerializer
            serializer.is_valid(raise_exception=True)
            serializer.save(mailbox=mailbox_obj)

            return HttpResponse(
                "Ok! Successfully saved to DB",
                status=200
            )

        # 유저가 잘못된 url을 입력하여 접근 (url에 적힌 random_strkey가 DB에 없음)
        except MailBox.DoesNotExist:
            return HttpResponse(
                "No! The requested mailbox not exists in DB",
                status=400
            )


class UpdateLetterView(APIView):  # 특정 편지 읽음 처리
    # 인증 & 허가 - JWTAuthentication, IsAuthenticated (기본 설정)

    def patch(self, request, letter_pk):
        letter = Letter.objects.get(pk=letter_pk)
        if letter.checked is not True:
            letter.checked = True
            letter.save()
            content = {'읽음처리 업데이트 성공'}
        else:
            content = {'이미 읽음처리 되었음'}
        return Response(content, status=status.HTTP_200_OK)
