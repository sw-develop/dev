from django.shortcuts import render
from mailboxapp.models import Mailbox
from rest_framework import viewsets
from mailboxapp.serializers import CreateMailBoxSerializer, ListMailBoxSerializer

# ViewSet 사용
# api 다 그냥 mailbox로 통일시켜버려... my-mailbox -> mailbox로 .. 그럼 한방에 처리 가능함!


class MailboxViewSet(viewsets.ModelViewSet):
    queryset = Mailbox.objects.all()

    # permission_classes 추가 필요

    # GenericAPIView클래스의 get_queryset() 메서드 오버라이딩
    def get_queryset(self):
        queryset = self.request.user.mailboxes.all() # 특정 사용자와 연관된 모든 우체통 객체 반환
        return queryset

    # Create, List Action
    # GenericAPIView클래스의 get_serializer_class() 메서드 오버라이딩
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateMailBoxSerializer
        if self.action == 'list':
            return ListMailBoxSerializer

    def list(self, request):



    # POST mailbox/<int:mailbox_pk>/secretkey