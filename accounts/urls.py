from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', log_in, name='login'),
    path('register/', register, name='register'),
    path("logout/", LogoutView.as_view(), name="logout"),
]
