from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from pathlib import Path
from logging import getLogger
from .forms import CompetitionForm
from .models import Competition
from django.contrib import messages

# Create your views here.

logger = getLogger(__name__)

COMPETITIONS_TABLE_TITLE = ['№ п/п', 'Краткое название', "Полное наименование", "Сроки",
                            "Активен", "Редактор"]


def edit_competitions(request):
    competitions = Competition.objects.all().order_by('name')
    context = dict()
    # print(competitions[0])
    # print(f"{competitions[0].date = }")

    # for comp in competitions:
    #     print(comp.date)
    context['competitions'] = competitions
    context['title'] = COMPETITIONS_TABLE_TITLE
    return render(request, 'app_for_competitions/edit_competitions.html', context=context)


def add_competition(request):
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


def competition_activate(request, pk):
    competition = Competition.objects.filter(id=pk).first()
    competition.active = not competition.active
    competition.save()
    messages.success(request, "Статус соревнования изменён")
    return redirect('all_competitions')


def delete_competition(request, pk):
    competition = Competition.objects.filter(id=pk)
    name = competition[0]
    competition.delete()
    logger.info(f"Соревнование {name} удалено")
    messages.success(request, f"Соревнование {name} удалено")
    return redirect('all_competitions')


def edit_competition(request, pk):
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
    context = {'title': "Результаты конкурса"}
    return render(request, 'app_for_competitions/competition_result.html', context)