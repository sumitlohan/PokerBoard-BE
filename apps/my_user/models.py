from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class my_user(AbstractUser):
    username = models.CharField(
        max_length=20,
        null = True
    )
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    updated_at = models.DateTimeField(('updated at'), default=timezone.now)
