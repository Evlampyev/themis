from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import LoginUser, logout_view, register

app_name = "users"

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
]
