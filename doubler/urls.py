from django.urls import path
from doubler.views import doubler

urlpatterns = [
    path('<int:number>/', doubler)
]
