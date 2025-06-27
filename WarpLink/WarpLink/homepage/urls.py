from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('server-status/', views.server_status, name='server_status'),
]
