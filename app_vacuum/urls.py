from django.urls import path
from app_vacuum.views import app_vacuum

urlpatterns = [
    path('', app_vacuum),
]
