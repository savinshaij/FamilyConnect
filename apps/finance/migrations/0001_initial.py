# Generated by Django 5.2.1 on 2025-06-08 04:38

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipFee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('month', models.DateField(help_text='Use the first of the month for grouping (e.g., 2025-06-01)')),
                ('paid_on', models.DateTimeField(auto_now_add=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('bank_transfer', 'Bank Transfer'), ('upi', 'UPI'), ('card', 'Card'), ('other', 'Other')], default='upi', max_length=30)),
                ('reference_id', models.CharField(blank=True, help_text='Transaction ID or reference number (for online payments)', max_length=100, null=True)),
                ('notes', models.TextField(blank=True, help_text='Optional notes by admin (e.g., payment remarks)', null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='groups.familygroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('verified_by', models.ForeignKey(blank=True, help_text='Admin who verified the payment', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verified_fees', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
