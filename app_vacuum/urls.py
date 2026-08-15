# vacuum/urls.py

from django.urls import path
from . import views

app_name = 'vacuum'

urlpatterns = [
    path('', views.check_vacuum_web, name='check_vacuum'),
    path('api/check_vacuum/', views.api_check_vacuum, name='api_check_vacuum'),
    ]
