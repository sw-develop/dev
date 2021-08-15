from django.db import models
from django.utils import timezone
from django.conf import settings


class AppUser(models.Model):
    kakao_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    birthdate = models.DateTimeField()
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)
    email = models.EmailField(blank=True, unique=True)
