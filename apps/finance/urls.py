# apps/finance/urls.py
from django.urls import path
from . import views

app_name = 'finance'  # important for namespacing

urlpatterns = [
    path('add_payment/<uuid:group_id>/', views.add_payment, name='add_payment'),
    # add other finance URLs here
]
