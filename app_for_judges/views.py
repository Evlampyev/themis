from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from logging import getLogger
from .forms import JudgeForm
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
# здесь не работает, не выбирает все соревнования
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
    """По сути должна быть регистрация судьи, но пока не реализована"""
    pass


def edit_judge(request, pk):
    """Редактирование судьи"""
    user = get_object_or_404(User, id=pk)

    if request.method == 'GET':
        context = {'form': JudgeForm(instance=user.judge,
                                     initial={'last_name': user.last_name, 'first_name': user.first_name}),
                   'id':pk}
        return render(request, 'app_for_judges/edit_judge.html', context)

    elif request.method == 'POST':
        form = JudgeForm(request.POST, instance=user)
        if form.is_valid():
            # temp_date = form.cleaned_data['date']
            # print(temp_date)
            # form.save()
            user.first_name = form.cleaned_data['first_name'].capitalize()
            user.judge.patronymic = form.cleaned_data['patronymic'].capitalize()
            user.last_name = form.cleaned_data['last_name'].capitalize()
            user.judge.post = form.cleaned_data['post']
            user.judge.regalia = form.cleaned_data['regalia']
            user.judge.organization = form.cleaned_data['organization']
            user.judge.status = form.cleaned_data['status']
            competition = form.cleaned_data['competition']
            # is_active = form.cleaned_data['is_active']
            user.save()
            if competition:
                user.judge.competitions.add(competition)
                # competition.judge_set.save(user)

            messages.success(request, 'Изменения сохранены')
            return redirect('all_judges')
        else:
            messages.error(request, 'Пожалуйста, исправьте следующие ошибки:')
            return render(request, 'app_for_judges/edit_judge.html', {'form': form})
