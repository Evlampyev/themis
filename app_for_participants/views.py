from django.shortcuts import render

# Create your views here.

def participants_list(request):
    context = {'title': 'Список участников'}
    return render(request, 'app_for_participants/participants_list.html', context)
