import random
import string

from datetime import date, timedelta
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import MailBox
from .serializers import CreateMailBoxSerializer, ListMailBoxSerializer, GetMailBoxSerializer
from letterapp.serializers import ListLetterSerializer


def get_random_open_date():  # 랜덤 우체통 공개 날짜 생성 메서드
    # 배포용
    # 우체통에 편지 작성 기한 : 우체통 생성 후 3일 뒤
    # 우체통 오픈 날짜 : 우체통 생성 후 5일 뒤
    mailbox_close_date = date.today() + timedelta(days=3)
    return mailbox_close_date + timedelta(days=2)

    # 테스트용 : 우체통 봉인 시점(우체통 생성 후 1일 뒤), 랜덤 날짜 조건(우체통 봉인 시점 + 1~2일 후)
    # mailbox_close_date = date.today() + timedelta(days=1)
    # return mailbox_close_date + timedelta(days=random.randint(1, 2))


def get_random_key():  # 우체통 별 랜덤 키 값 생성 메서드
    key_length = 8
    string_pool = string.ascii_lowercase + string.digits  # 소문자 + 숫자
    random_key = ""
    for i in range(key_length):
        random_key += random.choice(string_pool)
    return random_key


class MailBoxViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        app_user = self.request.user.app_user
        return MailBox.objects.filter(user=app_user)

    # GenericAPIView클래스의 get_serializer_class() 메서드 오버라이딩 - 조건에 맞는 Serializer 반환
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateMailBoxSerializer
        elif self.request.method == 'GET':
            if self.name == 'get_letters':
                return ListLetterSerializer
            return ListMailBoxSerializer

    """
    POST mailbox/ (우체통 생성) 
    """

    def create(self, request, *args, **kwargs):
        # 우체통 5개까지만 생성 가능 조건 추가
        if request.user.app_user.number_of_mailboxes() == 5:  # 수정 필요 사항 - AppUser 객체 내에 해당 메서드 생성하여 호출하기
            content = {'우체통 개수 초과하여 생성 불가'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)  # CreateMailBoxSerializer
        serializer.is_valid(raise_exception=True)

        mailbox = self.perform_create_mailbox(request, serializer)
        response_mailbox_serializer = GetMailBoxSerializer(mailbox)

        headers = self.get_success_headers(response_mailbox_serializer.data)
        return Response(response_mailbox_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create_mailbox(self, request, serializer):
        # user, link_title, open_date 값 추가하기
        mailbox = serializer.save(
            user=request.user.app_user,
            link_title=request.data['nickname'] + '의 우체통',
            open_date=get_random_open_date(),
        )
        # key, mailbox_link 필드에 값 추가
        random_key = get_random_key()
        mailbox.key = random_key
        mailbox.mailbox_link = mailbox.set_mailbox_link() + '/' + random_key
        mailbox.save()
        return mailbox

    """
    GET mailbox/ (개인의 모든 우체통 조회) - ModelViewSet 에 이미 정의되어 있음(수정 X) 
    """

    """
    GET mailbox/<int:mailbox_pk>/letters/ - 특정 우체통 편지 조회(=우체통 열기)
    """

    @action(detail=True, methods=['get'], url_path='letters', name='get_letters')
    def get_letters(self, request, pk=None):
        mailbox = MailBox.objects.get(pk=pk)
        mailbox.checked = True
        mailbox.save()

        queryset = mailbox.letters.all()  # 해당 우체통과 연관된 모든 편지 객체 반환
        first_letter = queryset.first()
        if first_letter is not None:
            first_letter.checked = True  # 첫 번째 편지 읽음 처리
            first_letter.save()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    DELETE mailbox/<int:mailbox_pk>/ - ModelViewSet 에 이미 정의되어 있음(수정 X)
    """

    """
    GET mailbox/totalLetter/ - 오픈되지 않은 우체통에 담긴 총 편지 개수 조회 
    """

    @action(detail=False, methods=['get'], url_path='totalLetter', name='total_letter')
    def total_letter(self, request):
        total_letter = request.user.app_user.number_of_letters_in_unopened_mailbox()

        return Response(
            data={'total_letter': total_letter},
            status=status.HTTP_200_OK
        )
