# vacuum/urls.py

from django.urls import path
from . import views

app_name = 'vacuum'

urlpatterns = [
    path('', views.check_vacuum, name='check_vacuum'),
]
