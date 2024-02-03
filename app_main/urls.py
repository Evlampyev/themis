from django.urls import path
from .views import home, about, base, contacts

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('base/', base, name='base'),
    path('contacts/', contacts, name='contacts'),
]
