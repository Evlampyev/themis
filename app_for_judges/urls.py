from django.urls import path
from .views import edit_judges, delete_judge, add_judge, edit_judge, participants_list, add_participant


urlpatterns = [
    path('all/', edit_judges, name='all_judges'),
    path('edit/<int:pk>/', edit_judge, name='edit_judge'),
    path('delete/<int:pk>/', delete_judge, name='delete_judge'),
    path('add/', add_judge, name='add_judge'),
    path('participants_list/<str:filter>', participants_list, name='participants_list'),
    path('add_participant', add_participant, name='add_participant'),
    # path('add/', RegisterUser.as_view(), name='add_judge'),

]
