from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin interface for the CustomUser model.
    Extends Django's default UserAdmin to include additional custom fields.
    """

    # Fields to display in the user list page
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'role', 'is_staff', 'is_active'
    )

    # Filters in the right sidebar
    list_filter = (
        'is_staff', 'is_active', 'role',
    )

    # Fields grouping in user detail/edit view
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {
            'fields': ('profile_picture_url', 'contact_info', 'role')
        }),
    )

    # Fields grouping in the user add view
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'profile_picture_url', 'contact_info', 'role'),
        }),
    )

    # Enable searching by these fields
    search_fields = ('email', 'username', 'first_name', 'last_name')

    # Default ordering
    ordering = ('email',)

# Register the custom user model with the customized admin
admin.site.register(CustomUser, CustomUserAdmin)
