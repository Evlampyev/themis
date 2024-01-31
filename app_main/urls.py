from django.urls import path
from .views import index, about, base

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('base/', base, name='base'),
]
