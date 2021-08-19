from django.db import models
from django.utils import timezone


class AppUser(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    birthdate = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    last_updated = models.DateTimeField(default=timezone.now, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    class Meta:
        db_table = 'user'
