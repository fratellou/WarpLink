from django.urls import path
from . import views

urlpatterns = [
    path('', views.download_config, name='download_config'),
]
