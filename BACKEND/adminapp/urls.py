from django.urls import path
from .views import MailView

app_name = "adminapp"

urlpatterns = [
    path('adminchk/', MailView.as_view()),
]
