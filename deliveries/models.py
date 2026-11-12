from django.db import models


class Delivery(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"
        DEAD = "dead", "Dead"

    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, related_name="deliveries")
    endpoint = models.ForeignKey("endpoints.Endpoint", on_delete=models.CASCADE, related_name="deliveries")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    attempt_count = models.PositiveIntegerField(default=0)
    next_attempt_at = models.DateTimeField(null=True, blank=True)
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "deliveries"
        constraints = [
            models.UniqueConstraint(fields=["event", "endpoint"], name="unique_delivery_per_endpoint"),
        ]

    def __str__(self):
        return f"{self.event} -> {self.endpoint} ({self.status})"


class DeliveryAttempt(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="attempts")
    attempt_number = models.PositiveIntegerField()
    status_code = models.PositiveIntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    duration_ms = models.PositiveIntegerField(null=True, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["attempt_number"]
        constraints = [
            models.UniqueConstraint(fields=["delivery", "attempt_number"], name="unique_attempt_number"),
        ]

    def __str__(self):
        return f"Attempt {self.attempt_number} of delivery {self.delivery_id}"
