import secrets

from django.conf import settings
from django.db import models


def generate_secret():
    return secrets.token_hex(32)


class Endpoint(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="endpoints")
    url = models.URLField(max_length=500)
    description = models.TextField(blank=True)
    event_types = models.JSONField(default=list, blank=True)
    secret = models.CharField(max_length=64, default=generate_secret, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.url
