from django.contrib import admin
from .models import Post, Comment, Like, PostType # Import PostType if you want to use it in admin

# --- Post Admin Configuration ---
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Fields to display in the list view of posts
    list_display = (
        'post_id',
        'content_snippet', # Custom method for a short content preview
        'post_type',
        'created_by_user',
        'group',
        'created_at',
        'likes_count',    # Method from the Post model
        'comments_count', # Method from the Post model
    )

    # Fields that can be filtered in the right sidebar
    list_filter = (
        'post_type',
        'created_at',
        'created_by_user',
        'group',
    )

    # Fields to search by
    search_fields = (
        'content',
        'created_by_user__username', # Search by username of the creator
        'group__group_name',         # Search by group name
    )

    # Fields to make clickable links to the detail view
    list_display_links = ('post_id', 'content_snippet',)

    # Fields that can be edited directly from the list view
    list_editable = ('post_type',)

    # Readonly fields in the detail view
    readonly_fields = ('post_id', 'created_at', 'last_edited_at')

    # Fieldsets for better organization in the detail view
    fieldsets = (
        (None, {
            'fields': ('post_type', 'content', 'media_attachments', 'group',)
        }),
        ('Audit Information', {
            'fields': ('post_id', 'created_by_user', 'created_at', 'last_edited_at'),
            'classes': ('collapse',) # Makes this section collapsible
        }),
        ('Advanced Visibility', {
            'fields': ('visibility_settings',),
            'classes': ('collapse',) # Makes this section collapsible
        })
    )

    # Automatically set the created_by_user to the current logged-in user
    def save_model(self, request, obj, form, change):
        if not obj.pk: # Only set on creation, not on update
            obj.created_by_user = request.user
        super().save_model(request, obj, form, change)

    # Custom method to display a snippet of the content
    def content_snippet(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_snippet.short_description = 'Content' # Admin column header


# --- Comment Admin Configuration ---
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'author',
        'content_snippet', # Custom method for a short content preview
        'created_at',
    )
    list_filter = (
        'created_at',
        'author',
        'post__created_by_user', # Filter comments by the author of the post they belong to
    )
    search_fields = (
        'content',
        'author__username',
        'post__content',
    )
    list_display_links = ('content_snippet',)
    readonly_fields = ('created_at',)

    def content_snippet(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_snippet.short_description = 'Comment Content'


# --- Like Admin Configuration ---
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'user',
        'created_at',
    )
    list_filter = (
        'created_at',
        'user',
        'post__created_by_user', # Filter likes by the author of the post they belong to
    )
    search_fields = (
        'user__username',
        'post__content',
    )
    readonly_fields = ('created_at',)