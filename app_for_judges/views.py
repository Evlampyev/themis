from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from logging import getLogger
# from .forms import UserForm
from .models import Judge
from django.contrib import messages
from django.urls import reverse

# Create your views here.


logger = getLogger(__name__)

JUDGE_TABLE_TITLE = ["№ п\п", 'Имя', "Отчество", "Фамилия", "Должность", "Заслуги",
                     "Место работы", "Статус", 'Соревнование', "Редактор"]


@login_required
def edit_judges(request):
    """Редактирование списка судей"""
    # @login_required - декоратор для проверки авторизации
    # user_status = request.user.judge.status # не нужно, получаю в шаблоне
    # users = Judge.objects.all()
    users = User.objects.filter(is_active=True).order_by('last_name')
    competitions_dict = {}
    for user in users:
        competitions_dict[user.pk] = [comp for comp in
                                       user.judge.competitions.all().values_list('name',
                                                                            flat=True)]
    context = {
        'title': JUDGE_TABLE_TITLE,
        'users': users,
        'competitions': competitions_dict,
        # 'user_status': user_status
    }
    return render(request, 'app_for_judges/edit_judges.html', context=context)


def delete_judge(request, pk):
    """Удаление судьи"""
    user = User.objects.get(id=pk)
    # judge.delete()
    # logger.info(f'{user} deleted')
    logger.info(f'{user.judge} deleted')
    user.is_active = False
    user.save()
    messages.success(request, f"Пользователь {user} удален ")
    return redirect('all_judges')


def add_judge(request):
    pass


def edit_judge(request, pk):
   pass
