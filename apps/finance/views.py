from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import GroupPayment
from apps.groups.models import FamilyGroup
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

@login_required
def add_payment(request, group_id):
    group = get_object_or_404(FamilyGroup, id=group_id)

    category_choices = ['membership', 'electricity', 'maintenance', 'other']

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category = request.POST.get('category', '').strip().lower()
        amount_str = request.POST.get('amount')
        user_id = request.POST.get('user_id')
        month_str = request.POST.get('month')
        status = request.POST.get('status', 'unpaid').lower()  
        method = request.POST.get('payment_method', 'upi')
        reference_id = request.POST.get('reference_id', '').strip()
        notes = request.POST.get('notes', '').strip()

    
        if not title:
            messages.error(request, "Title is required.")
            return redirect(reverse('groups:group_dashboard', args=[group.id]) + '?tab=finance')

        
        if category not in category_choices:
            category = 'other'

        
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except (InvalidOperation, ValueError):
            messages.error(request, "Invalid amount. Please enter a valid positive number.")
            return redirect(reverse('groups:group_dashboard', args=[group.id]) + '?tab=finance')

       
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "Selected user does not exist.")
            return redirect(reverse('groups:group_dashboard', args=[group.id]) + '?tab=finance')

       
        if not group.memberships.filter(user=user, status='approved').exists():
            messages.error(request, "Selected user is not an approved member of the group.")
            return redirect(reverse('groups:group_dashboard', args=[group.id]) + '?tab=finance')

       
        try:
           
            month = datetime.strptime(month_str, '%Y-%m').date().replace(day=1)
        except (ValueError, TypeError):
            messages.error(request, "Invalid month format.")
            return redirect(reverse('groups:group_dashboard', args=[group.id]) + '?tab=finance')

       
        GroupPayment.objects.create(
            group=group,
            user=user,
            title=title,
            category=category,
            amount=amount,
            month=month,
            status = 'paid' if request.POST.get('status') == 'paid' else 'unpaid',
            payment_method=method,
            reference_id=reference_id or None,
            notes=notes or None,
            is_confirmed=(status == 'paid'),
            verified_by=request.user if status == 'paid' else None,
            paid_on=now() if status == 'paid' else None
        )

        messages.success(request, "Payment recorded successfully.")
        return redirect(reverse('groups:group_dashboard', args=[group.id]) + '?tab=finance')

   
    return redirect(reverse('groups:group_dashboard', args=[group.id]) + '?tab=finance')
