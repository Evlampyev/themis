from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from logging import getLogger

from .forms import JudgeEditForm, UserAddForm, JudgeAddForm, ParticipantAddForm
from .models import Judge, Participant
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

# Create your views here.


logger = getLogger(__name__)

JUDGE_TABLE_TITLE = ["№ п\п", 'Имя', "Отчество", "Фамилия", "Должность", "Заслуги",
                     "Место работы", "Статус", 'Соревнование', "Редактор"]
PARTICIPANT_TABLE_TITLE = ["Фамилия", "Имя", 'Конкурс', 'Команда']


# class SimpleTable(tables.Table):
#    class Meta:
#       model = Judge
#
# def edit_judges(request):
#     table = SimpleTable(Judge.objects.all())
#     return render(request, 'app_for_judges/view_judges.html', {'table': table, 'title': 'Список судей'} )


@login_required
def judges_list(request, filter):
    """Список судей"""
    # @login_required - декоратор для проверки авторизации
    context = {'table_title': JUDGE_TABLE_TITLE}
    if filter == 'all':
        context['title'] = "Список организаторов"
        users = User.objects.filter(is_active=True).order_by('last_name')
    elif filter == 'judge':
        context['title'] = "Список судей"
        temp_users = User.objects.filter(is_active=True).order_by('last_name')
        users = []
        for user in temp_users:
            if user.judge.status == 'J':
                users.append(user)

    competitions_dict = {}
    for user in users:
        competitions_dict[user.pk] = [comp for comp in
                                      user.judge.competitions.all().values_list('name',
                                                                                flat=True)]
    context['users'] = users
    context['competitions'] = competitions_dict
    return render(request, 'app_for_judges/view_judges.html', context=context)


@login_required
def delete_judge(request, pk):
    """Удаление судьи"""
    user = User.objects.get(id=pk)
    logger.info(f'{user.judge} deleted')
    user.is_active = False
    user.save()
    messages.success(request, _(f"Пользователь {user} удален "))
    return redirect('all_judges')


@login_required
@transaction.atomic  # для транзакции - несколько операций базы данных в одну логическую единицу работы
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


@login_required
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


def participants_list(request, filter):
    """Список участников активных/всех соревнований"""
    context = {'title': 'Список участников'}
    if filter == 'active':
        participants = Participant.objects.filter(competition__active=True).order_by('competition', 'last_name')
        messages.success(request, _('Показаны участники активных соревнований'))
    elif filter == 'all':
        participants = Participant.objects.all().order_by('competition', 'last_name')
        messages.success(request, _('Показаны все участники'))
    context['participants'] = participants
    context['table_title'] = PARTICIPANT_TABLE_TITLE
    return render(request, 'app_for_judges/view_participants.html', context)


def add_participant(request):
    """Добавление участника"""
    title = 'Добавление участника'
    if request.method == 'POST':
        participant_form = ParticipantAddForm(request.POST)
        if participant_form.is_valid():
            participant = participant_form.save(commit=False)
            participant.save()
            logger.info(f'Participant {participant} added')
            messages.success(request, _('Участник добавлен'))
            return redirect('participants_list/all')
    else:
        participant_form = ParticipantAddForm()
    return render(request, 'app_for_judges/add_participant.html',
                  {'participant_form': participant_form, 'title': title})
