from django.conf import settings
from django.db import models


class Event(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    idempotency_key = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "idempotency_key"],
                condition=models.Q(idempotency_key__isnull=False),
                name="unique_idempotency_key_per_owner",
            )
        ]

    def __str__(self):
        return f"{self.event_type} ({self.id})"
