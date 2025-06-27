from django import forms

from apps.posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'media_attachments']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
