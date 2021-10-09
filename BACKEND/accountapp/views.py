import jwt
import requests
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from BACKEND.settings.local import SECRET_KEY  # local mode
from BACKEND.settings.deploy import SECRET_KEY  # deploy mode
from accountapp.models import AppUser

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import AddUserInfoSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


@method_decorator(csrf_exempt, name='dispatch')
class KakaoLoginView(View):  # 카카오 로그인
    permission_classes = [AllowAny]

    def post(self, request):
        access_token = request.headers["Authorization"]
        headers = ({'Authorization': f"Bearer {access_token}"})
        url = "https://kapi.kakao.com/v2/user/me"  # Authorization(프론트에서 받은 토큰)을 이용해서 회원의 정보를 확인하기 위한 카카오 API 주소
        response = requests.request("POST", url, headers=headers)  # API를 요청하여 회원의 정보를 response에 저장
        user_info_by_kakao = response.json()

        if User.objects.filter(username=user_info_by_kakao['id']).exists():  # 기존에 소셜로그인을 했었는지 확인
            AuthUser_obj = User.objects.get(username=user_info_by_kakao['id'])
            AppUser_obj = AppUser.objects.get(user=AuthUser_obj)

            encoded_jwt = jwt.encode({'id': AuthUser_obj.username}, SECRET_KEY, algorithm='HS256')  # jwt토큰 발행
            return JsonResponse({  # jwt토큰, 이름, 타입 프론트엔드에 전달
                'access_token': encoded_jwt,
                'user_name': AppUser_obj.name,
                'user_pk': AuthUser_obj.id
            }, status=200)

        else:
            new_AuthUser_obj = User.objects.create_user(
                username=user_info_by_kakao['id'],
                password=SECRET_KEY,
            )

            new_AppUser_obj = AppUser(
                user=new_AuthUser_obj,
                name=user_info_by_kakao['properties']['nickname'],
            )
            new_AppUser_obj.save()

            encoded_jwt = jwt.encode({'id': new_AuthUser_obj.username}, SECRET_KEY, algorithm='HS256')  # jwt토큰 발행
            return JsonResponse({  # jwt토큰, 이름, 타입 프론트엔드에 전달
                'access_token': encoded_jwt,
                'user_name': new_AppUser_obj.name,
                'user_pk': new_AuthUser_obj.id
            }, status=200)


class LoginView(APIView):  # 로그인
    permission_classes = [AllowAny]

    # 카카오톡에 사용자 정보 요청
    def getUserFromKakao(self, request):
        access_token = request.headers["Authorization"]
        headers = ({'Authorization': f"Bearer {access_token}"})
        url = "https://kapi.kakao.com/v2/user/me"
        response = requests.request("POST", url, headers=headers)  # POST 요청하여 회원 정보 response에 저장
        return response.json()

    # DB에 있는지 판별 (auth_user)
    def checkUserInDB(self, kakao_user):
        try:
            auth_user = User.objects.get(username=kakao_user['id'])
            app_user = AppUser.objects.get(pk=auth_user)
            return auth_user, app_user, True
        except User.DoesNotExist:  # 신규 회원일 때
            auth_user = User.objects.create_user(
                kakao_user['id'],
                'test@gmail.com',
                'poppymail'
            )
            app_user = AppUser.objects.create(user=User.objects.get(pk=auth_user.id))
            return auth_user, app_user, False

    # simple-JWT을 사용해 토큰 생성 해주는 역할만 수행하면 됨
    def createJWT(self, user):
        serializer = TokenObtainPairSerializer(data={'username': user.username, 'password': 'poppymail'})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return serializer.validated_data

    def post(self, request):
        kakao_user = self.getUserFromKakao(request)
        auth_user, app_user, check = self.checkUserInDB(kakao_user)

        if check:  # 기존 사용자
            is_new = 'false'
            if app_user.check_mailbox_today():
                check_mailbox_today = 'true'
            else:
                check_mailbox_today = 'false'
        else:  # 신규 사용자
            is_new = 'true'
            check_mailbox_today = 'false'

        response = self.createJWT(auth_user)

        return Response(
            data={
                'access': response['access'],
                'refresh': response['refresh'],
                'is_new': is_new,
                'user_id': auth_user.id,
                'username': app_user.name,
                'check_mailbox_today': check_mailbox_today
            },  # serializer.data와 동일한 형태
            status=status.HTTP_200_OK
        )


class AddUserInfoView(UpdateAPIView):  # 사용자 정보 추가 입력(업데이트)
    # 인증 & 허가 - JWTAuthentication, IsAuthenticated (기본 설정)

    queryset = AppUser.objects.all()
    serializer_class = AddUserInfoSerializer


class LogoutView(APIView):  # 로그아웃
    # 인증 & 허가 - JWTAuthentication, IsAuthenticated (기본 설정)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        content = {'로그아웃 성공'}
        return Response(content, status=status.HTTP_205_RESET_CONTENT)


class SignoutView(DestroyAPIView):  # 탈퇴
    # auth_user 삭제하면 -> AppUser, OutstandingToken, BlacklistedToken도 삭제됨 (서로 cascade로 설정되어 있음)
    # 인증 & 허가 - JWTAuthentication, IsAuthenticated (기본 설정)
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = User.objects.get(pk=request.user.id)
        self.perform_destroy(instance)
        content = {'탈퇴 완료'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


class KakaoLoginTestView(APIView):
    permission_classes = [AllowAny]

    # 카카오톡에 사용자 정보 요청
    def post(self, request):
        access_token = request.headers["Authorization"]
        headers = ({'Authorization': f"Bearer {access_token}"})
        url = "https://kapi.kakao.com/v2/user/me"
        response = requests.request("POST", url, headers=headers)  # POST 요청하여 회원 정보 response에 저장
        content = {'카카오 사용자 정보 요청 성공'}
        return Response(
            content,
            status=status.HTTP_200_OK
        )
