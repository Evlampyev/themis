from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from logging import getLogger

from django.template import RequestContext

from .forms import CompetitionForm, TableTaskForm, CompetitionTaskForm
from .models import Competition, CompetitionTask
from app_for_judges.models import TableTask, CompetitionResult
from django.contrib import messages

# Create your views here.

logger = getLogger(__name__)

COMPETITIONS_TABLE_TITLE = ["№\nп/п", 'Краткое название', "Полное наименование", "Сроки",
                            "Активен", "Редактор"]

RESULT_COMPETITION_TABLE_TITLE = ['Место', 'Участник', "Сумма мест"]


def edit_competitions(request):
    """Просмотр списка актуальных конкурсов"""
    competitions = Competition.objects.filter(date__gte=datetime.now()).order_by('-active', 'date')
    context = dict()
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
            name = form.cleaned_data['name']
            full_name = form.cleaned_data['fullname']
            date = form.cleaned_data['date']
            active = form.cleaned_data['active']
            comp = Competition(name=name, fullname=full_name, date=date, active=active)
            comp.save()
            logger.info(f'Добавили конкурс: {name}')
            messages.success(request, "Конкурс добавлен")
            return redirect('all_competitions')
    else:
        form = CompetitionForm()
    return render(request, 'app_for_competitions/edit_competition.html', {'form': form})


@login_required
def competition_activate(request, pk):
    """Активация/деактивация конкурса
    params: pk - id конкурса"""
    competition = Competition.objects.filter(id=pk).first()
    if competition.active:
        competition.active = False
        competition.save()
        CompetitionResult.objects.all().delete()  # очистка таблицы результатов конкурса
        competition_tasks = CompetitionTask.objects.filter(competition=competition)
        for task in competition_tasks:
            TableTask.objects.filter(competition_task=task).delete()  # очистка таблицы результатов этапа
            task.judging = True  # разрешение судейства
            task.save()
    else:
        competition.active = True
        competition.save()
        competitions = Competition.objects.exclude(id=pk)
        for comp in competitions:
            comp.active = False
            comp.save()
    logger.info(f"Статус соревнования изменён")
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
    """Результаты активного конкурса на Итоги"""
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
    context['active'] = competition.active
    return render(request, 'app_for_competitions/view_competition_tasks.html', context)


def get_title_and_fields_name(obj: object):
    """Получения заголовков полей таблицы результатов и
    названия этих полей
     :param obj: запись результата участника в таблице table_tasks
     """
    title = ['Участник']
    fields = ['participant']

    for index, (name, value) in enumerate(obj.items()):
        if name.startswith('name_') and value != "":
            title.append(value)
            fields.append(name[5:])

    title += ["Место", "Редактор"]
    fields += ['result_place']
    return title, fields


def get_ordering_table_task(competition_task, first, second):
    """
    Расстановка мест в таблице результатов
    :param competition_task: этап конкурса
    :param first: судить по графе первый параметр
    :param second: судить по графе второй параметр
    """
    result = TableTask.objects.filter(competition_task=competition_task).order_by(first, second)
    i = 1
    for row in result:
        row.result_place = i
        row.save()
        i += 1
    return result


def get_judging_categories(competition_task):
    """
    Выбор критериев сортировки для расстановки мест в таблице результатов
    """
    if competition_task.name_points != "":
        judging_criteria_first = '-points'  # судить по графе баллы по убыванию
    elif competition_task.name_total_time != "":
        judging_criteria_first = 'total_time'  # судить по графе время по возрастанию
    else:
        judging_criteria_first = 'average_time'  # судить по графе среднее время по возрастанию

    if competition_task.name_correction_time != "":
        judging_criteria_second = 'correction_time'  # корректировать по времени
    elif competition_task.name_correction_score_up != "":
        judging_criteria_second = '-correction_score_up'  # корректировать по баллам вверх
    else:
        judging_criteria_second = 'correction_score_down'  # корректировать по баллам вниз

    return judging_criteria_first, judging_criteria_second


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

    comp_task_as_dict = CompetitionTask.objects.filter(id=pk).values()
    my_obj = comp_task_as_dict[0]
    task_table_title, fields_name = get_title_and_fields_name(my_obj)  # получение заголовков таблицы и имен полей

    judging_criteria_first, judging_criteria_second = get_judging_categories(competition_task)
    table_task = get_ordering_table_task(competition_task, judging_criteria_first, judging_criteria_second)

    # table_task = TableTask.objects.filter(competition_task=competition_task).order_by(
    #     judging_criteria_first, judging_criteria_second)  # таблица результатов
    # i = 1
    # for row in table_task:
    #     row.result_place = i
    #     row.save()
    #     i += 1
    context = {'title': f"{competition.name}",
               'competition_task': competition_task.name,
               'pk': competition_task.id,
               'table': table_task,
               'table_title': task_table_title}

    if request.method == 'POST':
        form = TableTaskForm(request.POST)
        if form.is_valid():
            # print(f"{fields_name = }")
            # dict_table_task = {k: None for k in fields_name}

            participant = form.cleaned_data['participant']
            intermediate_points_1 = form.cleaned_data['intermediate_points_1']
            intermediate_points_2 = form.cleaned_data['intermediate_points_2']
            intermediate_points_3 = form.cleaned_data['intermediate_points_3']
            intermediate_points_4 = form.cleaned_data['intermediate_points_4']
            points = form.cleaned_data['points']
            correction_score_up = form.cleaned_data['correction_score_up']
            correction_score_down = form.cleaned_data['correction_score_down']
            intermediate_time_1 = form.cleaned_data['intermediate_time_1']
            intermediate_time_2 = form.cleaned_data['intermediate_time_2']
            average_time = form.cleaned_data['average_time']
            total_time = form.cleaned_data['total_time']
            correction_time = form.cleaned_data['correction_time']

            # for key, value in dict_table_task.items():
            #     if key != "result_place":
            #         dict_table_task[key] = form.cleaned_data[f"{key}"]
            # print(f"{dict_table_task = }")

            table_task = TableTask(competition_task=competition_task, participant=participant,
                                   intermediate_points_1=intermediate_points_1,
                                   intermediate_points_2=intermediate_points_2,
                                   intermediate_points_3=intermediate_points_3,
                                   intermediate_points_4=intermediate_points_4,
                                   points=points, correction_score_up=correction_score_up,
                                   correction_score_down=correction_score_down, intermediate_time_1=intermediate_time_1,
                                   intermediate_time_2=intermediate_time_2, average_time=average_time,
                                   total_time=total_time, correction_time=correction_time)
            table_task.save()
            # table_task = get_ordering_table_task(competition_task, judging_criteria_first, judging_criteria_second)
            # table_task = TableTask.objects.filter(competition_task=competition_task).order_by(
            #     judging_criteria_first, judging_criteria_second)  # таблица результатов
            # i = 1
            # for row in table_task:
            #     row.result_place = i
            #     row.save()
            #     i += 1
            logger.info(f'Добавлен результат участника {participant}')
            messages.success(request, f"Результат  {participant} добавлен")
            return redirect('judge_task', pk=pk, pc=pc)
        else:
            print("Форма не валидна")
            print(form.errors)
            messages.error(request, f"Не верные данные для ввода: {form.errors}")
            return redirect('judge_task', pk=pk, pc=pc)

    else:
        form = TableTaskForm()
        context['form'] = form
        context['fields_name'] = fields_name
        return render(request, 'app_for_competitions/judge_task.html', context)


def create_competition_task(request, pc: int):
    """Создание этапа конкурса"""
    competition = get_object_or_404(Competition, id=pc)
    if request.method == 'POST':
        form = CompetitionTaskForm(request.POST)
        if form.is_valid():
            competition_task = CompetitionTask(competition=competition, name=form.cleaned_data['name'],
                                               judging=form.cleaned_data['judging'],
                                               name_intermediate_points_1=form.cleaned_data[
                                                   'name_intermediate_points_1'],
                                               name_intermediate_points_2=form.cleaned_data[
                                                   'name_intermediate_points_2'],
                                               name_intermediate_points_3=form.cleaned_data[
                                                   'name_intermediate_points_3'],
                                               name_intermediate_points_4=form.cleaned_data[
                                                   'name_intermediate_points_4'],
                                               name_points=form.cleaned_data['name_points'],
                                               name_correction_score_up=form.cleaned_data['name_correction_score_up'],
                                               name_correction_score_down=form.cleaned_data[
                                                   'name_correction_score_down'],
                                               name_intermediate_time_1=form.cleaned_data['name_intermediate_time_1'],
                                               name_intermediate_time_2=form.cleaned_data['name_intermediate_time_2'],
                                               name_average_time=form.cleaned_data['name_average_time'],
                                               name_total_time=form.cleaned_data['name_total_time'],
                                               name_correction_time=form.cleaned_data['name_correction_time']
                                               )
            competition_task.save()
            logger.info(f': Task {competition_task.name} created')
            messages.success(request, f'Этап конкурса "{competition.name}" добавлен')
            return redirect('view_competition', pk=pc)
    else:
        form = CompetitionTaskForm()
    return render(request, 'app_for_competitions/create_competition_task.html', {'form': form})


def view_task_result(request, pk: int, pc: int):
    """Просмотр результатов этапа конкурса
    params: pk - id этапа
            pc - id конкурса
    """
    competition = Competition.objects.filter(id=pc).first()  # конкурс
    competition_task = CompetitionTask.objects.filter(id=pk).first()  # этап конкурса

    judging_criteria_first, judging_criteria_second = get_judging_categories(competition_task)  # судить по графе
    table_task = get_ordering_table_task(competition_task, judging_criteria_first,
                                         judging_criteria_second)  # таблица результатов

    comp_task_as_dict = CompetitionTask.objects.filter(id=pk).values()

    my_obj = comp_task_as_dict[0]
    task_table_title, fields_name = get_title_and_fields_name(my_obj)

    context = {'title': f"{competition.name}",
               'competition_task': competition_task.name,
               'table': table_task,
               'table_title': task_table_title,
               'fields_name': fields_name}

    # print(f'{fields_name = }')
    return render(request, 'app_for_competitions/view_task_result.html', context)


def delete_participant_from_table_task(request, pk):
    """Удаление пользователя из таблицы результатов этапа конкурса"""
    row_in_table = TableTask.objects.filter(id=pk)
    # competition_task_id = row_in_table[0].competition_task.id
    row_in_table.delete()
    # competition_id = CompetitionTask.objects.filter(id=competition_task_id).first().competition.id
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # перезагрузка той страницы, где происходит действие
