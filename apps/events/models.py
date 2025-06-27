import uuid
from django.db import models
from django.conf import settings
from apps.groups.models import FamilyGroup  # adjust path if needed

class Event(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='events')
    event_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    rsvp_options = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.event_name} ({self.start_time.strftime('%Y-%m-%d')})"
