from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    vpn_credits = models.IntegerField(default=1)
