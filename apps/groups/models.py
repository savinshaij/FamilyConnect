import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class FamilyGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_family_groups'
    )
    
    admin_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='admin_of_family_groups'
    )
    
    is_public = models.BooleanField(default=False)
    invitation_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.group_name


class GroupMembership(models.Model):
    class MembershipStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        LEFT = 'left', 'Left'
    
    class MembershipRole(models.TextChoices):
        MEMBER = 'member', 'Member'
        ADMIN = 'admin', 'Admin'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='family_group_memberships'
    )
    
    group = models.ForeignKey(
        FamilyGroup,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    
    status = models.CharField(
        max_length=10,
        choices=MembershipStatus.choices,
        default=MembershipStatus.PENDING
    )
    
    role = models.CharField(
        max_length=10,
        choices=MembershipRole.choices,
        default=MembershipRole.MEMBER
    )
    
    joined_at = models.DateTimeField(default=timezone.now)
    
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_memberships'
    )

    class Meta:
        unique_together = ('user', 'group')
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user} ({self.role}) in {self.group} - {self.status}"
