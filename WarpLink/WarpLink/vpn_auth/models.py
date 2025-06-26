from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    vpn_credits = models.IntegerField(default=1)
