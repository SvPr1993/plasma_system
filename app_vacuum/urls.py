# vacuum/urls.py

from django.urls import path
from . import views

app_name = 'vacuum'

urlpatterns = [
    path('', views.check_vacuum_web, name='check_vacuum'),
    path('api/check_vacuum/', views.api_check_vacuum, name='api_check_vacuum'),
    path('api/check_vacuum_async/', views.api_check_vacuum_async, name='api_check_vacuum_async'),
    path('api/task/<str:task_id>/', views.get_task_result, name='task_result'),
    ]
