from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.http import require_POST
from apps.groups.models import FamilyGroup
from .models import Post, Comment, Like, PostType

@login_required
def view_posts(request, group_id):
    group = get_object_or_404(FamilyGroup, id=group_id)

    # Check group access permissions
    if not group.is_public and not group.memberships.filter(user=request.user, status='approved').exists():
        return render(request, '403.html', status=403)

    # Get all posts and prefetch related data for performance
    posts = Post.objects.filter(group=group).select_related(
        'created_by_user', 'group'
    ).prefetch_related(
        'likes', 'comments', 'comments__author'
    ).order_by('-created_at')

    post_data = []
    for post in posts:
        # Check if user can delete each comment (author or admin)
        comments_with_permissions = []
        for comment in post.comments.all().order_by('created_at'):
            comments_with_permissions.append({
                'comment': comment,
                'can_delete': (
                    comment.author == request.user or 
                    group.admin_user == request.user
                )
            })
        
        post_data.append({
            'post': post,
            'comments': comments_with_permissions,
            'user_has_liked': post.likes.filter(user=request.user).exists(),
            'can_delete': (
                post.created_by_user == request.user or 
                group.admin_user == request.user
            ),
            'like_count': post.likes.count(),
            'comment_count': post.comments.count(),
        })

    return render(request, 'posts/view_posts.html', {
        'group': group,
        'post_data': post_data,
        'post_types': PostType.choices,
        'is_group_admin': group.admin_user == request.user,
    })


@login_required
def add_post(request, group_id):
    group = get_object_or_404(FamilyGroup, id=group_id)

    if not group.is_public and not group.memberships.filter(user=request.user, status='approved').exists():
        return render(request, '403.html', status=403)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        post_type = request.POST.get('post_type', PostType.FAMILY_GROUP_SPECIFIC)
        media_urls = []

        # Validate content
        if not content:
            messages.error(request, "Content is required to create a post.")
            return redirect(reverse('posts:add_post', kwargs={'group_id': group_id}))

        # Handle file uploads
        if 'media_attachments' in request.FILES:
            for file in request.FILES.getlist('media_attachments'):
                if file.size > 5 * 1024 * 1024:  # 5MB limit
                    messages.error(request, f"File {file.name} is too large (max 5MB).")
                    continue
                
                try:
                    path = default_storage.save(
                        f'posts/{group_id}/{timezone.now().timestamp()}_{file.name}',
                        ContentFile(file.read())
                    )
                    media_urls.append(default_storage.url(path))
                except Exception as e:
                    messages.error(request, f"Error uploading {file.name}: {str(e)}")

        # Create post
        post = Post.objects.create(
            post_type=post_type,
            content=content,
            created_by_user=request.user,
            group=group,
            media_attachments=media_urls if media_urls else None
        )

        messages.success(request, "Post created successfully.")
        return redirect(reverse('posts:view_posts', kwargs={'group_id': group_id}))

    return render(request, 'posts/add_post.html', {
        'group': group,
        'post_types': PostType.choices,
    })


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    group = post.group

    is_admin = group.admin_user == request.user
    is_author = post.created_by_user == request.user

    if not (is_admin or is_author):
        return render(request, '403.html', status=403)

    # Delete associated media files
    if post.media_attachments:
        for url in post.media_attachments:
            try:
                path = url.split('/media/')[-1]  # Extract relative path
                default_storage.delete(path)
            except Exception as e:
                messages.error(request, f"Error deleting media file: {str(e)}")

    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect(reverse('posts:view_posts', kwargs={'group_id': group.id}))


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)

    # Check permissions based on post type
    if post.post_type == PostType.FAMILY_GROUP_SPECIFIC and not post.group.memberships.filter(user=request.user, status='approved').exists():
        return render(request, '403.html', status=403)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if not content:
            messages.error(request, "Comment cannot be empty.")
        else:
            Comment.objects.create(
                post=post, 
                author=request.user, 
                content=content
            )
            messages.success(request, "Comment added successfully.")

    return redirect(reverse('posts:view_posts', kwargs={'group_id': post.group.id}))


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    group = comment.post.group

    is_admin = group.admin_user == request.user
    is_author = comment.author == request.user

    if not (is_admin or is_author):
        return render(request, '403.html', status=403)

    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect(reverse('posts:view_posts', kwargs={'group_id': group.id}))


@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)

    # Check permissions based on post type
    if post.post_type == PostType.FAMILY_GROUP_SPECIFIC and not post.group.memberships.filter(user=request.user, status='approved').exists():
        return JsonResponse({'error': 'Permission denied'}, status=403)

    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like.delete()
        action = 'unliked'
    else:
        action = 'liked'

    like_count = post.likes.count()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'action': action,
            'like_count': like_count,
            'user_has_liked': created
        })

    messages.success(request, f"You {action} the post.")
    return redirect(reverse('posts:view_posts', kwargs={'group_id': post.group.id}))