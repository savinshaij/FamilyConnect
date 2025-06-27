from django.urls import path
from . import views


app_name = 'core'
urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('home/', views.home_page, name='home'),
   
   
]
