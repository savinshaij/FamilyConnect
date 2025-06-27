from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'created_by', 'created_at', 'group')
    search_fields = ('title', 'content')
    list_filter = ('document_type', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
