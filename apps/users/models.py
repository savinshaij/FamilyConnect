from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    USER = 'USER', _('User')
    PLATFORM_ADMIN = 'PLATFORM_ADMIN', _('Platform Admin')

class CustomUser(AbstractUser):
    profile_picture_url = models.URLField(
        _('profile picture URL'),
        max_length=200,
        blank=True,
        null=True,
        help_text=_("URL to the user's profile picture (optional).")
    )
    contact_info = models.JSONField(
        _('contact information'),
        blank=True,
        null=True,
        help_text=_('Additional contact details (phone, address, etc).')
    )
    role = models.CharField(
        _('user role'),
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
        help_text=_("User's role on the platform.")
    )
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username or self.email or str(self.pk)

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        return self.first_name or self.username
