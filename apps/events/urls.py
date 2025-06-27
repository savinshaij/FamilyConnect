from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('<uuid:group_id>/add/', views.add_event, name='add_event'),
]
