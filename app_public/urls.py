from django.urls import path
from . import views

app_name = 'app_public'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    ]