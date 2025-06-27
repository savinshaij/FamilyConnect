from django.contrib import admin
from .models import GroupPayment


@admin.register(GroupPayment)
class GroupPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'group', 'category', 'amount', 'status', 'month', 'payment_method',
        'paid_on', 'is_confirmed', 'verified_by'
    )
    list_filter = (
        'category', 'status', 'payment_method', 'is_confirmed', 'month', 'group'
    )
    search_fields = (
        'user__username', 'reference_id', 'notes', 'verified_by__username'
    )
    ordering = ('-paid_on',)

    readonly_fields = ('paid_on',)

    fieldsets = (
        (None, {
            'fields': ('user', 'group', 'category', 'amount', 'status', 'month', 'paid_on')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'reference_id', 'notes')
        }),
        ('Verification', {
            'fields': ('is_confirmed', 'verified_by')
        }),
    )
