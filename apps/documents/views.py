from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.groups.models import FamilyGroup
from .models import Document, DocumentType

@login_required
def create_document(request, group_id):
    group = get_object_or_404(FamilyGroup, id=group_id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '')
        document_type = request.POST.get('document_type')
        uploaded_file = request.FILES.get('file')

        if not title or not document_type:
            messages.error(request, "Title and document type are required.")
            return redirect(f'/groups/{group.id}/dashboard/?tab=add_documents')

        Document.objects.create(
            title=title,
            content=content,
            file=uploaded_file,
            created_by=request.user,
            document_type=document_type,
            group=group if document_type == DocumentType.FAMILY_GROUP_SPECIFIC else None
        )

        messages.success(request, "Document uploaded successfully.")
        return redirect(f'/groups/{group.id}/dashboard/?tab=documents')

    return redirect(f'/groups/{group.id}/dashboard/?tab=add_document')
