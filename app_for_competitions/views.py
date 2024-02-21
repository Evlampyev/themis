from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from logging import getLogger
from .forms import CompetitionForm, TableTaskForm
from .models import Competition, CompetitionTask
from app_for_judges.models import TableTask, CompetitionResult
from django.contrib import messages

# Create your views here.

logger = getLogger(__name__)

COMPETITIONS_TABLE_TITLE = ['№ п/п', 'Краткое название', "Полное наименование", "Сроки",
                            "Активен", "Редактор"]
TASK_TABLE_TITLE = ['Участник', "Время, \nмм:сс", "Место", "Редактор"]

RESULT_COMPETITION_TABLE_TITLE = ['Место', 'Участник', "Сумма мест"]


def edit_competitions(request):
    """Просмотр списка конкурсов"""
    competitions = Competition.objects.all().order_by('name')
    context = dict()
    # print(competitions[0])
    # print(f"{competitions[0].date = }")

    # for comp in competitions:
    #     print(comp.date)
    context['competitions'] = competitions
    context['table_title'] = COMPETITIONS_TABLE_TITLE
    context['title'] = "Конкурсы"

    return render(request, 'app_for_competitions/view_competitions.html', context=context)


@login_required
def add_competition(request):
    """Добавление конкурса"""
    if request.method == 'POST':
        form = CompetitionForm(request.POST)
        if form.is_valid():
            # form.save()
            name = form.cleaned_data['name']
            full_name = form.cleaned_data['fullname']
            date = form.cleaned_data['date']
            active = form.cleaned_data['active']
            comp = Competition(name=name, fullname=full_name, date=date, active=active)
            comp.save()
            # logger.info(f'Добавили {form.cleaned_data["name"]}')
            logger.info(f'Добавили конкурс: {name}')
            messages.success(request, "Конкурс добавлен")
            return redirect('all_competitions')
    else:
        form = CompetitionForm()
    return render(request, 'app_for_competitions/edit_competition.html', {'form': form})


@login_required
def competition_activate(request, pk):
    """Активация конкурса
    params: pk - id конкурса"""
    competition = Competition.objects.filter(id=pk).first()
    competition.active = not competition.active
    competition.save()
    messages.success(request, "Статус соревнования изменён")
    return redirect('all_competitions')


@login_required
def delete_competition(request, pk):
    """Удаление конкурса
    params: pk - id конкурса"""
    competition = Competition.objects.filter(id=pk)
    name = competition[0]
    competition.delete()
    logger.info(f"Соревнование {name} удалено")
    messages.success(request, f"Соревнование {name} удалено")
    return redirect('all_competitions')


@login_required
def edit_competition(request, pk):
    """Редактирование конкурса
    params: pk - id конкурса"""
    competition = get_object_or_404(Competition, id=pk)

    if request.method == 'GET':
        context = {'form': CompetitionForm(instance=competition), 'id': pk}
        return render(request, 'app_for_competitions/edit_competition.html', context)

    elif request.method == 'POST':
        form = CompetitionForm(request.POST, instance=competition)
        if form.is_valid():
            competition.name = form.cleaned_data['name']
            competition.fullname = form.cleaned_data['fullname']
            competition.date = form.cleaned_data['date']
            competition.active = form.cleaned_data['active']
            competition.save()
            messages.success(request, f"Изменения сохранены")
            return redirect('all_competitions')
        else:
            messages.error(request, 'Пожалуйста, исправьте следующие ошибки:')
            return render(request, 'app_for_competitions/edit_competition.html', {'form': form})


def competition_result(request):
    """Результаты конкурса на Итоги"""
    context = {'title': "Результаты конкурса"}
    competition = Competition.objects.filter(active=True).first()
    context['competition'] = competition
    context['table_title'] = RESULT_COMPETITION_TABLE_TITLE

    competition_results = CompetitionResult.objects.all().order_by('final_place')
    context['competition_results'] = competition_results

    return render(request, 'app_for_competitions/competition_result.html', context)


def view_competition(request, pk):
    """Просмотр всех этапов конкурса"""
    competition = get_object_or_404(Competition, id=pk)
    context = {'title': f"{competition.name}"}
    competition_tasks = CompetitionTask.objects.filter(competition=competition)
    context['competition_tasks'] = competition_tasks
    context['competition_id'] = pk
    return render(request, 'app_for_competitions/view_competition_tasks.html', context)


def end_judging(request, pk: int):
    """Завершение судейства для этапа конкурса
    :param pk: id этапа конкурса
    """
    competition_task = get_object_or_404(CompetitionTask, id=pk)
    participants = TableTask.objects.filter(competition_task=competition_task)
    for row_participant in participants:
        participant_in_results = CompetitionResult.objects.filter(participant=row_participant.participant).first()
        if participant_in_results:
            participant_in_results.final_place += row_participant.result_place
            participant_in_results.save()
        else:
            competition_res = CompetitionResult()
            competition_res.participant = row_participant.participant
            competition_res.final_place = row_participant.result_place
            competition_res.save()

    competition_task.judging = False
    competition_task.save()
    return redirect('competition_result')


@login_required
def judge_task(request, pk, pc):
    """Судейство этапа конкурса
    params: pk - id этапа
            pc - id конкурса
    """
    competition = Competition.objects.filter(id=pc).first()  # конкурс
    competition_task = CompetitionTask.objects.filter(id=pk).first()  # этап конкурса
    table_task = TableTask.objects.filter(competition_task=competition_task).order_by('time')  # таблица результатов

    context = {'title': f"{competition.name}",
               'competition_task': competition_task.name,
               'pk': competition_task.id,
               'table': table_task,
               'table_title': TASK_TABLE_TITLE}

    if request.method == 'POST':
        form = TableTaskForm(request.POST)
        if form.is_valid():
            participant = form.cleaned_data['participant']
            time = form.cleaned_data['time']
            table_task = TableTask(competition_task=competition_task, participant=participant, time=time)
            table_task.save()
            table_task = TableTask.objects.filter(competition_task=competition_task).order_by(
                'time')  # таблица результатов
            i = 1
            for row in table_task:
                row.result_place = i
                row.save()
                i += 1
            messages.success(request, f"Результат  {participant} добавлен")
            return redirect('judge_task', pk=pk, pc=pc)
    else:
        form = TableTaskForm()
        context['form'] = form
        return render(request, 'app_for_competitions/judge_task.html', context)


def view_task_result(request, pk, pc):
    """Просмотр результатов этапа конкурса
    params: pk - id этапа
            pc - id конкурса
    """
    competition = Competition.objects.filter(id=pc).first()  # конкурс
    competition_task = CompetitionTask.objects.filter(id=pk).first()  # этап конкурса
    table_task = TableTask.objects.filter(competition_task=competition_task).order_by(
        'participant')  # таблица результатов

    context = {'title': f"{competition.name}",
               'competition_task': competition_task.name,
               'table': table_task,
               'table_title': TASK_TABLE_TITLE}

    return render(request, 'app_for_competitions/view_task_result.html', context)
