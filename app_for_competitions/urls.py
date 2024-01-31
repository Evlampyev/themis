from django.urls import path
from .views import edit_competitions, add_competition, competition_activate, delete_competition, \
    edit_competition

urlpatterns = [

    path('all/', edit_competitions, name='all_competitions'),
    path('add/', add_competition, name='add_competition'),
    path('delete/<int:pk>/', delete_competition, name='delete_competition'),
    path('edit/<int:pk>/', edit_competition, name='edit_competition'),
    path('activate/<int:pk>/', competition_activate, name='competition_activate'),
    # path('about/index', index, name='index'),

]
