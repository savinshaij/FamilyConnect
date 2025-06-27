import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.groups.models import FamilyGroup # Assuming your FamilyGroup model is here

class DocumentType(models.TextChoices):
    PRIVATE = 'PRIVATE', _('Private')
    FAMILY_GROUP_SPECIFIC = 'FAMILY_GROUP_SPECIFIC', _('Family Group Specific')


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, help_text=_("Title of the document."))
   
    content = models.TextField(blank=True, help_text=_("Optional description or notes for the document."))

   
    file = models.FileField(
        upload_to='documents/', 
        null=True,             
        blank=True,           
        help_text=_("Upload a file (e.g., PDF, image, spreadsheet).")
    )
 
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_documents',
        help_text=_("The user who created this document.")
    )

    created_at = models.DateTimeField(default=timezone.now, help_text=_("Timestamp when the document was created."))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("Timestamp when the document was last updated."))

    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
        default=DocumentType.PRIVATE,
        help_text=_("Defines who can view this document (Private or Group Specific).")
    )

    group = models.ForeignKey(
        FamilyGroup,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='documents',
        help_text=_("The family group this document is associated with (if group specific).")
    )

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_private(self):
        return self.document_type == DocumentType.PRIVATE

    def is_group_specific(self):
        return self.document_type == DocumentType.FAMILY_GROUP_SPECIFIC

    # Optional: Method to get file URL
    def get_file_url(self):
        if self.file:
            return self.file.url
        return None