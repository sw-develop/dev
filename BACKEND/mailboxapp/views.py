import random
import string

from mailboxapp.models import Mailbox
from requests import Response
from rest_framework import viewsets, status
from mailboxapp.serializers import CreateMailBoxSerializer, ListMailBoxSerializer, GetMailBoxSerializer, CheckMailBoxKeySerializer

from datetime import date
from rest_framework.decorators import action

# ViewSet 사용
# api 다 그냥 mailbox로 통일시켜버려... my-mailbox -> mailbox로 .. 그럼 한방에 처리 가능함!

def get_random_open_date():  # 랜덤 우체통 공개 날짜 생성 메서드
    # 랜덤 날짜 조건 : 우체통 봉인 시점(우체통 생성 후 3일 뒤)부터 1주일 ~ 1달 후
    mailbox_close_date = date.today() + 3
    return mailbox_close_date + random.randint(7, 30)


def get_random_key():  # 랜덤 우체통 비밀키 값 생성 메서드
    key_length = 6
    string_pool = string.ascii_lowercase  # 소문자
    secret_key = ""
    for i in range(key_length):
        secret_key += random.choice(string_pool)
    return secret_key


class MailboxViewSet(viewsets.ModelViewSet):
    # permission_classes 추가 필요

    # GenericAPIView클래스의 get_queryset() 메서드 오버라이딩
    def get_queryset(self):
        queryset = self.request.user.mailboxes.all()  # 특정 사용자와 연관된 모든 우체통 객체 반환
        return queryset

    # Create, List Action
    # GenericAPIView클래스의 get_serializer_class() 메서드 오버라이딩 - 조건에 맞는 Serializer 반환
    def get_serializer_class(self):
        if self.action == 'create':
            if self.name == 'check_secret_key':
                return CheckMailBoxKeySerializer
            return CreateMailBoxSerializer
        if self.action == 'list':
            return ListMailBoxSerializer

    """
    POST mailbox (우체통 생성) 
    """
    def perform_create_mailbox(self, request, serializer):
        # user, link_title, open_date, key 필드에 값 추가하기
        mailbox = serializer.save(
            user=request.user,  # 추가 - Authentication 추가해야 사용 가능함
            link_title=request.data['nickname'] + '의 우체통',
            open_date=get_random_open_date(),
            key=get_random_key()
        )
        # mailbox_link 필드에 값 추가
        mailbox.mailbox_link = mailbox.set_mailbox_link()
        return mailbox.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # CreateMailBoxSerializer
        serializer.is_valid(raise_exception=True)

        mailbox = self.perform_create_mailbox(serializer)
        response_mailbox_serializer = GetMailBoxSerializer(mailbox)

        headers = self.get_success_headers(response_mailbox_serializer.data)
        return Response(response_mailbox_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    """
    GET mailbox (개인의 모든 우체통 조회) - ModelViewSet 에 이미 정의되어 있음(수정 X) 
    """

    """
    POST mailbox/<int:mailbox_pk>/secretkey -> Serializer 필요 X 
    """
    @action(detail=True, methods=['post'], name='check_secret_key', url_path='secretkey')
    def check_secret_key(self, request, pk=None):
        serializer



