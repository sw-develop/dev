from django.urls import path
from .views import KakaoLoginView

app_name = "accountapp"

urlpatterns = [
    path('login/kakao/', KakaoLoginView.as_view()),
]
