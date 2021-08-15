from django.db import models
from django.utils import timezone


class SocialPlatform(models.Model):
    platform = models.CharField(max_length=20, default=0)

    class Meta:
        db_table = "social_platform"


class AppUser(models.Model):
    social = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, max_length=20, blank=True, default=1)
    social_login_id = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    birthdate = models.DateTimeField()
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)
    email = models.EmailField(blank=True, unique=True)
