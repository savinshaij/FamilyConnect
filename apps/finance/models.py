from django.db import models
from django.conf import settings
from apps.groups.models import FamilyGroup
import uuid

class PaymentStatus(models.TextChoices):
    PAID = 'paid', 'Paid'
    UNPAID = 'unpaid', 'Unpaid'

class GroupPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Title and category
    title = models.CharField(max_length=100, help_text="Short title or label for the payment")
    category = models.CharField(max_length=100, help_text="Category of the payment (e.g., Membership, Electricity)")

    amount = models.DecimalField(max_digits=8, decimal_places=2)
    month = models.DateField(help_text="Use the 1st of the month for grouping (e.g., 2025-06-01)")
    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID,
        help_text="Payment status"
    )
    paid_on = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)

    payment_method = models.CharField(
        max_length=30,
        choices=[
            ('cash', 'Cash'),
            ('bank_transfer', 'Bank Transfer'),
            ('upi', 'UPI'),
            ('card', 'Card'),
            ('other', 'Other')
        ],
        default='upi'
    )
    reference_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Transaction ID or reference number (for online payments)"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Optional notes by admin (e.g., payment remarks)"
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='verified_payments',
        help_text="Admin who verified the payment"
    )

    class Meta:
        verbose_name = "Group Payment"
        verbose_name_plural = "Group Payments"
        ordering = ['-month', 'category']

    def __str__(self):
        return f"{self.title} - {self.user.username} - {self.month.strftime('%B %Y')} - ₹{self.amount} - {self.status.capitalize()}"
