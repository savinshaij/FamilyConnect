import uuid
import os
from django.db import models
from django.conf import settings
from apps.groups.models import FamilyGroup

def memory_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("memories", unique_filename)

class Memory(models.Model):
    group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='memories')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=memory_image_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.group})"
