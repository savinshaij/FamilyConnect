# posts/urls.py
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # Change int:group_id to uuid:group_id
    path('group/<uuid:group_id>/', views.view_posts, name='view_posts'),
    path('group/<uuid:group_id>/add/', views.add_post, name='add_post'),
    
    # Keep the rest of your URLs the same
    path('post/<uuid:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<uuid:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<uuid:post_id>/like/', views.toggle_like, name='toggle_like'),
]