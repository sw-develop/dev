from django.urls import path
from .views import LetterRequestView, UpdateLetterView

app_name = "letterapp"

urlpatterns = [
    path('letter/<int:mailbox_pk>/<str:random_strkey>/', LetterRequestView.as_view(), name="letter_request"),
    path('letter/<int:letter_pk>/', UpdateLetterView.as_view())
]
