from django.urls import path
from app_ballon.views import app_ballon

urlpatterns = [
    path('', app_ballon),
]
