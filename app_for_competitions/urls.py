from django.urls import path
from .views import edit_competitions, add_competition, competition_activate, delete_competition, \
    edit_competition,competition_result, view_competition, view_task_result, judge_task

urlpatterns = [

    path('all/', edit_competitions, name='all_competitions'),
    path('add/', add_competition, name='add_competition'),
    path('delete/<int:pk>/', delete_competition, name='delete_competition'),
    path('edit/<int:pk>/', edit_competition, name='edit_competition'),
    path('activate/<int:pk>/', competition_activate, name='competition_activate'),
    path('competition_result/', competition_result, name='competition_result'),
    path('view_competition/<int:pk>/', view_competition, name='view_competition'),
    path('view_competition/<int:pc>/<int:pk>/', view_task_result, name='view_task_result'),
    path('judge_task/<int:pc>/<int:pk>/', judge_task, name='judge_task'),

]
