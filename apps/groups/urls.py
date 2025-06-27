from django.urls import path
from . import views

app_name = "groups"

urlpatterns = [
    path("create/", views.create_group, name="create_group"),
    path("join/", views.join_group_by_code, name="join_group"),

    # Dashboard main with optional tab param (posts, add_post, etc.)
     # Dashboard main with tab system
    path('<uuid:group_id>/dashboard/', views.group_dashboard, name='group_dashboard'),
   


    
    path("approve/<uuid:membership_id>/", views.approve_request, name="approve_request"),
    path("reject/<uuid:membership_id>/", views.reject_request, name="reject_request"),
    path("<uuid:group_id>/leave/", views.leave_group, name="leave_group"),
    path("remove/<uuid:member_id>/", views.remove_member, name="remove_member"),
    path("make-admin/<uuid:member_id>/", views.make_admin, name="make_admin"),
    path('delete/<uuid:group_id>/', views.delete_group, name='delete_group'),
    path('remove-admin/<uuid:member_id>/', views.remove_admin, name='remove_admin'),



    path('post/<uuid:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<uuid:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<uuid:post_id>/like/', views.toggle_like, name='toggle_like'),

]
