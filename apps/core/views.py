from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone
from dataclasses import dataclass
from itertools import chain

from apps.groups.models import FamilyGroup, GroupMembership
from apps.posts.models import Post,PostType
from apps.events.models import Event

User = get_user_model()


@dataclass
class Activity:
    type: str
    timestamp: timezone.datetime
    obj: object


def landing_page(request):
    return render(request, 'core/landing.html')


@login_required
def home_page(request):
    user = request.user

    # Get user’s approved group memberships
    memberships = GroupMembership.objects.select_related('group').filter(
        user=user,
        status=GroupMembership.MembershipStatus.APPROVED
    )

    group_ids = memberships.values_list('group_id', flat=True)

    # Sidebar group data
    groups = []
    for membership in memberships:
        group = membership.group
        groups.append({
            'id': group.id,
            'name': group.group_name,
            'description': group.description,
            'members_count': group.memberships.filter(
                status=GroupMembership.MembershipStatus.APPROVED
            ).count(),
            'joined_date': membership.joined_at.date(),
            'type': 'Public' if group.is_public else 'Private',
        })

    # Build activity feed using Activity dataclass
    activity_feed = []

    # Recent Posts
    posts = Post.objects.select_related('group', 'created_by_user').filter(
    group_id__in=group_ids,
    post_type=PostType.FAMILY_GROUP_SPECIFIC  # ← correct way
).order_by('-created_at')[:5]


    for post in posts:
        activity_feed.append(Activity("Post", post.created_at, post))

    # Recent Events
    events = Event.objects.select_related('group', 'created_by_user').filter(
        group_id__in=group_ids
    ).order_by('-start_time')[:5]

    for event in events:
        activity_feed.append(Activity("Event", event.start_time, event))

    # Recent Group Joins
    joins = GroupMembership.objects.select_related('user', 'group').filter(
        group_id__in=group_ids,
        status=GroupMembership.MembershipStatus.APPROVED
    ).order_by('-joined_at')[:5]

    for join in joins:
        activity_feed.append(Activity("Join", join.joined_at, join))

    # Sort unified feed
    activity_feed.sort(key=lambda x: x.timestamp, reverse=True)

    activity_feed = activity_feed[:4]

    context = {
        'user': user,
        'groups': groups,
        'range_list': range(1, 7),
        'activity_feed': activity_feed,
    }

    return render(request, 'core/home.html', context)
