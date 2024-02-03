from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from logging import getLogger
from .forms import JudgeEditForm, UserAddForm, JudgeAddForm
from .models import Judge
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.utils.translation import gettext_lazy as _

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
    return render(request, 'app_for_judges/view_judges.html', context=context)


def delete_judge(request, pk):
    """Удаление судьи"""
    user = User.objects.get(id=pk)
    # judge.delete()
    # logger.info(f'{user} deleted')
    logger.info(f'{user.judge} deleted')
    user.is_active = False
    user.save()
    messages.success(request, _(f"Пользователь {user} удален "))
    return redirect('all_judges')


@login_required
@transaction.atomic
def add_judge(request):
    """Добавление судьи"""
    title = "Добавление судьи"
    if request.method == "POST":
        user_form = UserAddForm(request.POST)
        # чтобы заполнять все поля при регистрации используется вторая форма JudgeAddForm, но там проблема с сохранением соревнований судьи.
        # judge_form = JudgeAddForm(request.POST)
        # if user_form.is_valid() and judge_form.is_valid():
        if user_form.is_valid:
            user = user_form.save(commit=False)
            user.is_active = True
            user.save()
            # user.judge.patronymic = judge_form.cleaned_data['patronymic'].capitalize()
            # user.judge.post = judge_form.cleaned_data['post']
            # user.judge.regalia = judge_form.cleaned_data['regalia']
            # user.judge.organization = judge_form.cleaned_data['organization']
            # user.judge.status = judge_form.cleaned_data['status']
            # competitions = judge_form.cleaned_data['competitions']
            # print(f'{user.judge.organization}')
            # print(f'{competitions = }')
            # # Не сохраняются соревнования, остальное вроде есть
            # judge = Judge.objects.get(id=user.judge.id)
            # if competitions:
            #     competitions.set.add(judge)
            # user.save()
            logger.info(f'{user} добавлен.')
            messages.success(request, _('Судья добавлен'))
            return redirect('all_judges')

    else:
        user_form = UserAddForm()
        # judge_form = JudgeAddForm()
    return render(request, 'app_for_judges/add_judge.html',
                  {'user_form': user_form, 'title': title})


# class RegisterUser(CreateView):
#     form_class = UserRegisterForm
#     template_name = 'app_for_judges/edit_judge.html'
#     extra_context = {'title': "Регистрация судьи"}
#     success_url = reverse_lazy('all_judges')


def edit_judge(request, pk):
    """Редактирование судьи"""
    user = get_object_or_404(User, id=pk)

    if request.method == 'GET':
        context = {'form': JudgeEditForm(instance=user.judge,
                                         initial={'last_name': user.last_name, 'first_name': user.first_name}),
                   'id': pk}
        return render(request, 'app_for_judges/edit_judge.html', context)

    elif request.method == 'POST':
        form = JudgeEditForm(request.POST, instance=user)
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

            messages.success(request, _('Изменения сохранены'))
            return redirect('all_judges')
        else:
            messages.error(request, _('Пожалуйста, исправьте следующие ошибки:'))
            return render(request, 'app_for_judges/edit_judge.html', {'form': form})


def participants_list(request):
    context = {'title': 'Список участников'}
    return render(request, 'app_for_judges/view_participants.html', context)