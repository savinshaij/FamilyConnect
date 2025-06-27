from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Memory
from apps.groups.models import FamilyGroup


@login_required
def add_memory(request, group_id):
    group = get_object_or_404(FamilyGroup, id=group_id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('image')

        
        if not title:
            messages.error(request, "Title is required.")
            return redirect(f"{request.path}?tab=add_memory")

        if not image:
            messages.error(request, "An image is required to create a memory.")
            return redirect(f"{request.path}?tab=add_memory")

        try:
            memory = Memory.objects.create(
                group=group,
                created_by=request.user,
                title=title,
                description=description,
                image=image
            )
            messages.success(request, "Memory added successfully.")
        except ValidationError as e:
            messages.error(request, f"Error saving memory: {e}")
        except Exception as e:
            messages.error(request, "An unexpected error occurred while adding the memory.")

        return redirect(f'/groups/{group.id}/dashboard/?tab=memories', group_id=group.id)

    # If GET request, redirect to dashboard directly (prevent form rendering outside dashboard)
    return redirect(f'/groups/{group.id}/dashboard/?tab=memories', group_id=group.id)
