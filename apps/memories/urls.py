from django.urls import path
from . import views

app_name = "memories"

urlpatterns = [
    path('<uuid:group_id>/add/', views.add_memory, name='add_memory'),
]
