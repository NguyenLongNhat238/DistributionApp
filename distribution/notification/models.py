from django.db import models
from django.conf import settings

# Create your models here.


class Notification(models.Model):
    TYPE_INFO = "info"
    TYPE_WARNING = "warning"
    TYPE_ERROR = "error"
    TYPE_SUCCESS = "success"

    TYPE_NOTIFICATION = (
        ("info", "Info"),
        ("warning", "Warning"),
        ("error", "Error"),
        ("success", "Success"),
    )
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # sender
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    # receiver
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_NOTIFICATION)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ("-created_at",)
