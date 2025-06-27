from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.groups.models import FamilyGroup  # adjust if your model is located elsewhere
from .models import Event  # your Event model
from django.utils import timezone

@login_required
def add_event(request, group_id):
    group = get_object_or_404(FamilyGroup, id=group_id)

    if request.method == 'POST':
        event_name = request.POST.get('event_name', '').strip()
        description = request.POST.get('description', '')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location', '')

        if not event_name or not start_time:
            messages.error(request, "Event name and start time are required.")
            return redirect('groups:group_dashboard', group_id=group.id)

        Event.objects.create(
            group=group,
            event_name=event_name,
            description=description,
            start_time=start_time,
            end_time=end_time or None,
            location=location,
            created_by_user=request.user
        )

        messages.success(request, "Event added successfully.")
        return redirect(f'/groups/{group.id}/dashboard/?tab=events', group_id=group.id)

    return redirect(f'/groups/{group.id}/dashboard/?tab=events', group_id=group.id)
