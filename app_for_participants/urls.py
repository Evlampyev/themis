from django.urls import path
from .views import participants_list

urlpatterns = [
    path('', participants_list, name='participants_list'),
]
