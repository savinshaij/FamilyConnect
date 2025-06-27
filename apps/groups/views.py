from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.db import transaction
from .forms import PostForm
from .models import FamilyGroup, GroupMembership
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.http import require_POST
from apps.groups.models import FamilyGroup
from apps.posts.models import Post, Comment, Like, PostType
from apps.events.models import Event
from apps.finance.models import GroupPayment 
from apps.memories.models import Memory
from django.core.exceptions import ValidationError
from django.db.models import Q
from apps.documents.models import Document, DocumentType
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import json
import uuid

def is_group_admin(user, group):
    return GroupMembership.objects.filter(user=user, group=group, role=GroupMembership.MembershipRole.ADMIN).exists()


@login_required
def create_group(request):
    if request.method == "POST":
        group_name = request.POST.get("group_name")
        description = request.POST.get("description", "")
        is_public = request.POST.get("is_public") == "on"

        # Generate unique invitation code
        invitation_code = get_random_string(length=8)
        while FamilyGroup.objects.filter(invitation_code=invitation_code).exists():
            invitation_code = get_random_string(length=8)

        group = FamilyGroup.objects.create(
            group_name=group_name,
            description=description,
            created_by=request.user,
            admin_user=request.user,
            is_public=is_public,
            invitation_code=invitation_code
        )

        GroupMembership.objects.create(
            user=request.user,
            group=group,
            status=GroupMembership.MembershipStatus.APPROVED,
            role=GroupMembership.MembershipRole.ADMIN,
            approved_by=request.user
        )

        messages.success(request, f"Group '{group_name}' created successfully!")
        return redirect('groups:group_dashboard', group_id=group.id)

    return render(request, "groups/create_group.html")


@login_required
def join_group_by_code(request):
    if request.method == "POST":
        code = request.POST.get("invitation_code")
        group_id = request.POST.get("group_id")

        group = None
        if code:
            group = FamilyGroup.objects.filter(invitation_code=code).first()
            if not group:
                messages.error(request, "Invalid invitation code.")
                return redirect('groups:join_group')
        elif group_id:
            group = get_object_or_404(FamilyGroup, id=group_id)
        else:
            messages.error(request, "Please enter a valid code or group ID.")
            return redirect('groups:join_group')

        if GroupMembership.objects.filter(user=request.user, group=group).exists():
            messages.info(request, "You are already a member or have requested to join.")
            return redirect('groups:group_dashboard', group_id=group.id)

        GroupMembership.objects.create(
            user=request.user,
            group=group,
            status=GroupMembership.MembershipStatus.PENDING,
            role=GroupMembership.MembershipRole.MEMBER
        )

        messages.success(request, f"Request to join group '{group.group_name}' sent.")
        return redirect('groups:group_dashboard', group_id=group.id)

    return render(request, "groups/join_group.html")


@login_required
def group_dashboard(request, group_id):
    active_tab = request.GET.get('tab', 'posts')
    group = get_object_or_404(FamilyGroup, id=group_id)

    try:
        membership = GroupMembership.objects.select_related('group', 'user').get(
            user=request.user,
            group=group,
            status=GroupMembership.MembershipStatus.APPROVED
        )
    except GroupMembership.DoesNotExist:
        messages.error(request, "You do not have access to this group.")
        return redirect('core:home')

    is_admin = membership.role == GroupMembership.MembershipRole.ADMIN

    approved_members = group.memberships.filter(
        status=GroupMembership.MembershipStatus.APPROVED
    ).select_related('user')

    pending_requests = (
        group.memberships.filter(status=GroupMembership.MembershipStatus.PENDING)
        .select_related('user') if is_admin else []
    )

   
    context = {
        "group": group,
        "members": approved_members,
        "pending_requests": pending_requests,
        "membership": membership,
        "is_admin": is_admin,
        'active_tab': active_tab,
        "event_count": Event.objects.filter(group=group).order_by('start_time').count(),
        
        
    }
    if active_tab == 'posts':
        
        posts = Post.objects.filter(
            Q(post_type=PostType.FAMILY_GROUP_SPECIFIC, group=group) |
            Q(post_type=PostType.PRIVATE, created_by_user=request.user) |
            
            
        Q(post_type=PostType.PUBLIC)
        ).select_related(
        'created_by_user', 'group'
        ).prefetch_related(
        'likes', 'comments', 'comments__author'
        ).order_by('-created_at')


        post_data = []
        for post in posts:
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

        context.update({
            'post_data': post_data,
            'post_types': PostType.choices,
            'is_group_admin': group.admin_user == request.user,
        })

    elif active_tab == 'events':
        context['events'] = Event.objects.filter(group=group).order_by('start_time')

    elif active_tab == 'add_event':
        context['post_types'] = PostType.choices  # optional context
    elif active_tab == 'add_finance':
        context['members'] = group.memberships.filter(status='approved').select_related('user')
  # For dropdown in form

    elif active_tab == 'finance':
        payments = GroupPayment.objects.filter(group=group) \
            .select_related('user', 'verified_by') \
            .order_by('-month')
        context['payments'] = payments
    elif active_tab == 'documents':
        documents = Document.objects.filter(
            Q(document_type=DocumentType.FAMILY_GROUP_SPECIFIC, group=group) |
            Q(document_type=DocumentType.PRIVATE, created_by=request.user)
        ).select_related('created_by').order_by('-created_at')

        context['documents'] = documents


    elif active_tab == 'add_document':
        context['document_types'] = DocumentType.choices


    elif active_tab == 'memories':
        context['memories'] = Memory.objects.filter(
        group=group
    ).select_related('created_by').order_by('-created_at')

    elif active_tab == 'add_memory':
   
        pass
    
    elif active_tab == 'add_post':
        if request.method == 'POST':
            content = request.POST.get('content', '').strip()
            post_type = request.POST.get('post_type', PostType.FAMILY_GROUP_SPECIFIC)
            media_urls = []

            if not content:
                messages.error(request, "Content is required to create a post.")
                return redirect(f"{request.path}?tab=add_post")

            # Validate post type
            if post_type not in [PostType.FAMILY_GROUP_SPECIFIC, PostType.PRIVATE, PostType.PUBLIC]:
                messages.error(request, "Invalid post type selected.")
                return redirect(f"{request.path}?tab=add_post")


            # Handle file uploads
            if 'media_attachments' in request.FILES:
                for file in request.FILES.getlist('media_attachments'):
                    if file.size > 10 * 1024 * 1024:  # 10MB limit
                        messages.error(request, f"File {file.name} is too large (max 10MB).")
                        continue
                    try:
                        path = default_storage.save(
                            f'posts/{group_id}/{timezone.now().timestamp()}_{file.name}',
                            ContentFile(file.read())
                        )
                        media_urls.append(default_storage.url(path))
                    except Exception as e:
                        messages.error(request, f"Error uploading {file.name}: {str(e)}")

            # Save post
            Post.objects.create(
                post_type=post_type,
                content=content,
                created_by_user=request.user,
                group=group,
                media_attachments=media_urls if media_urls else None
            )

            messages.success(request, "Post created successfully.")
            return redirect(f"{request.path}?tab=posts")

        context.update({
            'post_types': PostType.choices,
        })

    return render(request, "groups/group_dashboard.html", context)



@login_required
def approve_request(request, membership_id):
    membership = get_object_or_404(GroupMembership, id=membership_id)

    if not is_group_admin(request.user, membership.group):
        messages.error(request, "Only the group admin can approve requests.")
        return redirect('groups:group_dashboard', group_id=membership.group.id)

    if membership.status != GroupMembership.MembershipStatus.PENDING:
        messages.warning(request, "This request has already been processed.")
        return redirect('groups:group_dashboard', group_id=membership.group.id)

    # Update membership
    membership.status = GroupMembership.MembershipStatus.APPROVED
    membership.approved_by = request.user
    membership.joined_at = timezone.now()
    membership.save()

    # ✅ Send welcome email
    # subject = f"Welcome to {membership.group.group_name}!"
    # message = (
    #     f"Hi {membership.user.first_name},\n\n"
    #     f"Your request to join the group '{membership.group.group_name}'  has been approved.\n"
    #     f"We're happy to have you with us!\n\n"
    #     f"Cheers,\nFamilyConnect Team"
    # )
    # recipient_list = [membership.user.email]

    # send_mail(
    #     subject,
    #     message,
    #     'dev.savinshaij@gmail.com',
    #     recipient_list,
    #     fail_silently=False,
    # )
    send_approval_email(request, membership)
    messages.success(request, f"{membership.user} has been approved and notified via email.")
    return redirect('groups:group_dashboard', group_id=membership.group.id)


@login_required
def reject_request(request, membership_id):
    membership = get_object_or_404(GroupMembership, id=membership_id)
    if not is_group_admin(request.user, membership.group):
        messages.error(request, "Only group admin can reject requests.")
        return redirect('groups:group_dashboard', group_id=membership.group.id)

    membership.status = GroupMembership.MembershipStatus.REJECTED
    membership.approved_by = request.user
    membership.save()
    messages.success(request, f"{membership.user.username}'s request was rejected.")
    return redirect('groups:group_dashboard', group_id=membership.group.id)


@login_required
def leave_group(request, group_id):
    group = get_object_or_404(FamilyGroup, id=group_id)
    membership = GroupMembership.objects.filter(group=group, user=request.user).first()

    if membership.role == GroupMembership.MembershipRole.ADMIN:
        admin_count = GroupMembership.objects.filter(group=group, role=GroupMembership.MembershipRole.ADMIN).count()
        if admin_count <= 1:
            messages.error(request, "You are the only admin. Assign another admin before leaving.")
            return redirect('groups:group_dashboard', group_id=group.id)

    membership.delete()
    messages.success(request, "You have left the group.")
    return redirect('core:home')



@login_required
def remove_member(request, member_id):
    member = get_object_or_404(GroupMembership, id=member_id)
    if not is_group_admin(request.user, member.group):
        messages.error(request, "Only admins can remove members.")
        return redirect('groups:group_dashboard', group_id=member.group.id)

    member.delete()
    messages.success(request, "Member removed successfully.")
    return redirect('groups:group_dashboard', group_id=member.group.id)


@login_required
def make_admin(request, member_id):
    member = get_object_or_404(GroupMembership, id=member_id)
    if not is_group_admin(request.user, member.group):
        messages.error(request, "Only admins can promote others.")
        return redirect('groups:group_dashboard', group_id=member.group.id)

    member.role = GroupMembership.MembershipRole.ADMIN
    member.save()
    messages.success(request, f"{member.user.username} is now an admin.")
    return redirect('groups:group_dashboard', group_id=member.group.id)

@login_required
def remove_admin(request, member_id):
    member = get_object_or_404(GroupMembership, id=member_id)
    group = member.group

    if not is_group_admin(request.user, group):
        messages.error(request, "Only admins can remove admin roles.")
        return redirect('groups:group_dashboard', group_id=group.id)

    if member.user == request.user:
        messages.error(request, "You cannot remove your own admin role.")
        return redirect('groups:group_dashboard', group_id=group.id)

    if member.role != GroupMembership.MembershipRole.ADMIN:
        messages.error(request, "This user is not an admin.")
        return redirect('groups:group_dashboard', group_id=group.id)

    admin_count = GroupMembership.objects.filter(group=group, role=GroupMembership.MembershipRole.ADMIN).count()
    if admin_count <= 1:
        messages.error(request, "At least one admin must remain.")
        return redirect('groups:group_dashboard', group_id=group.id)

    if request.method == "POST":
        member.role = GroupMembership.MembershipRole.MEMBER
        member.save()
        messages.success(request, f"{member.user.username} is no longer an admin.")

    return redirect('groups:group_dashboard', group_id=group.id)


@login_required
def delete_group(request, group_id):
    group = get_object_or_404(FamilyGroup, id=group_id)

    if not is_group_admin(request.user, group):
        messages.error(request, "Only admins can delete the group.")
        return redirect('groups:group_dashboard', group_id=group.id)

    if request.method == "POST":
        group.delete()
        messages.success(request, "Group deleted successfully.")
        return redirect('core:home')

    return render(request, "groups/confirm_delete.html", {"group": group})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    group = post.group

    is_admin = group.admin_user == request.user
    is_author = post.created_by_user == request.user

    if not (is_admin or is_author):
        return render(request, '403.html', status=403)

   
    if post.media_attachments:
        for url in post.media_attachments:
            try:
                path = url.split('/media/')[-1]  
                default_storage.delete(path)
            except Exception as e:
                messages.error(request, f"Error deleting media file: {str(e)}")

    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('groups:group_dashboard', group_id=group.id)

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
    return redirect('groups:group_dashboard', group_id=post.group.id)

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
    return redirect('groups:group_dashboard', group_id=group.id)

    

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)

    # Check permissions 
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
    return redirect('groups:group_dashboard', group_id=post.group.id)





def send_approval_email(request, membership):
    subject = f"Welcome to {membership.group.group_name}!"
    from_email = 'dev.savinshaij@gmail.com'
    to_email = [membership.user.email]

    # Build the URL here, not in the template
    group_url = request.build_absolute_uri(
        reverse('groups:group_dashboard', args=[membership.group.id])
    )

    context = {
        'user': membership.user,
        'group': membership.group,
        'group_url': group_url,
    }

    html_content = render_to_string('emails/group_approval_email.html', context)
    text_content = f"""
    Hi {membership.user.first_name},

    Your request to join the group '{membership.group.group_name}' has been approved.

    Visit your group: {group_url}

    - FamilyConnect Team
    """

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)