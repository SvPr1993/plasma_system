from django.urls import path

from app_ballon import views
from app_ballon.views import app_ballon

urlpatterns = [
    path('', views.app_ballon, name='app_ballon'),
]
