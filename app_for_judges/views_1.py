from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
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
    # judges = Judge.objects.all()
    judges = Judge.objects.filter(is_active=True).order_by('last_name')
    competitions_dict = {}
    for judge in judges:
        competitions_dict[judge.pk] = [comp for comp in
                                       judge.competitions.all().values_list('name',
                                                                            flat=True)]
    context = {
        'title'       : JUDGE_TABLE_TITLE,
        'judges'      : judges,
        'competitions': competitions_dict
    }
    return render(request, 'app_for_judges/edit_judges.html', context=context)


def delete_judge(request, pk):
    """Удаление судьи"""
    judge = Judge.objects.get(id=pk)
    print(f" For delete {judge = }")
    # judge.delete()
    logger.info(f'{judge} deleted')
    judge.is_active = False
    judge.save()
    messages.success(request, "Пользователь удален")
    return redirect('all_judges')


def add_judge(request):
    """Добавление судьи"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].capitalize()
            patronymic = form.cleaned_data['patronymic'].capitalize()
            last_name = form.cleaned_data['last_name'].capitalize()
            post = form.cleaned_data['post']
            regalia = form.cleaned_data['regalia']
            organization = form.cleaned_data['organization']
            status = form.cleaned_data['status']
            competition = form.cleaned_data['competition']
            # is_active = form.cleaned_data['is_active']
            # comp = Competition.objects.filter(name=competition)
            judge = Judge(name=name, patronymic=patronymic, last_name=last_name,
                          organization=organization, post=post, regalia=regalia,
                          status=status)
            judge.save()
            if competition:
                competition.judge_set.add(judge)
            # добавляет в поле со связью многие ко многим
            logger.info(f'Получили данные {"name"} {last_name}.')

            messages.success(request, 'Судья добавлен')
            return redirect('all_judges')

    else:
        form = UserForm()
    return render(request, 'app_for_judges/edit_judge.html', {'form': form})


def edit_judge(request, pk):
    """Редактирование судьи"""
    judge = get_object_or_404(Judge, id=pk)

    if request.method == 'GET':
        context = {'form': UserForm(instance=judge), 'id': pk}
        return render(request, 'app_for_judges/edit_judge.html', context)

    elif request.method == 'POST':
        form = UserForm(request.POST, instance=judge)
        if form.is_valid():
            # temp_date = form.cleaned_data['date']
            # print(temp_date)
            # form.save()
            judge.name = form.cleaned_data['name'].capitalize()
            judge.patronymic = form.cleaned_data['patronymic'].capitalize()
            judge.last_name = form.cleaned_data['last_name'].capitalize()
            judge.post = form.cleaned_data['post']
            judge.regalia = form.cleaned_data['regalia']
            judge.organization = form.cleaned_data['organization']
            judge.status = form.cleaned_data['status']
            competition = form.cleaned_data['competition']
            # is_active = form.cleaned_data['is_active']
            judge.save()
            if competition:
                judge.competitions.add(competition)
                # competition.judge_set.save(judge)

            messages.success(request, 'Изменения сохранены')
            return redirect('all_judges')
        else:
            messages.error(request, 'Пожалуйста, исправьте следующие ошибки:')
            return render(request, 'app_for_judges/edit_judge.html', {'form': form})
