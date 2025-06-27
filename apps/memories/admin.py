from django.contrib import admin
from .models import Memory

@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'created_by', 'created_at')
    list_filter = ('group', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('group', 'created_by')
