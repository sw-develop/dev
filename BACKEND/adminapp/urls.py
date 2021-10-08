from django.urls import path
from .views import MailView

app_name = "adminapp"

urlpatterns = [
    path('userstocheck/', MailView.as_view()),
]
