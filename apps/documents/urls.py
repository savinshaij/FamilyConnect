from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('upload/<uuid:group_id>/', views.create_document, name='create_document'),
]
