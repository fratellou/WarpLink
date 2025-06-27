from django.db import models
from django.conf import settings


class VPNConfig(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    ovpn_file = models.FileField(upload_to='ovpn_files/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Конфиг для {self.user.username}'
