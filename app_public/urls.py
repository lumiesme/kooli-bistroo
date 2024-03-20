from django.urls import path
from . import views

app_name = 'app_public'

urlpatterns = [
    path("", views.HomeViewPublic.as_view(), name="index"),
]

handler404 = 'app_public.views.error_404'
handler500 = 'app_public.views.error_500'
