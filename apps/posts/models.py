import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import CustomUser
from apps.groups.models import FamilyGroup


class PostType(models.TextChoices):
    PUBLIC = 'PUBLIC', _('Public')
    PRIVATE = 'PRIVATE', _('Private')
    FAMILY_GROUP_SPECIFIC = 'GROUP_SPECIFIC', _('Family Group Specific')


class Post(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    post_type = models.CharField(
        _('post type'),
        max_length=20,
        choices=PostType.choices,
        default=PostType.FAMILY_GROUP_SPECIFIC,
        help_text=_("Defines the audience/scope of the post.")
    )

    content = models.TextField(_('content'), help_text=_("The main text content of the post."))

    media_attachments = models.JSONField(
        _('media attachments'),
        blank=True,
        null=True,
        default=list,
        help_text=_("JSON array of URLs to images or videos attached to the post.")
    )

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    created_by_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('created by user')
    )

    group = models.ForeignKey(
        FamilyGroup,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True,
        verbose_name=_('group'),
        help_text=_("The family group this post belongs to, if applicable.")
    )

    visibility_settings = models.JSONField(
        _('visibility settings'),
        blank=True,
        null=True,
        help_text=_('JSON for more granular visibility rules (e.g., specific members).')
    )

    last_edited_at = models.DateTimeField(_('last edited at'), auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-created_at']

    def __str__(self):
        group_name = self.group.group_name if self.group else 'General'
        return f"Post by {self.created_by_user.username} in {group_name} on {self.created_at.strftime('%Y-%m-%d')}"

    def likes_count(self):
        return self.likes.count()

    def comments_count(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('post')
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('author')
    )
    content = models.TextField(_('comment content'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name=_('post')
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name=_('user')
    )
    created_at = models.DateTimeField(_('liked at'), auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
        verbose_name = _('like')
        verbose_name_plural = _('likes')

    def __str__(self):
        return f"{self.user.username} liked post {self.post.post_id}"

