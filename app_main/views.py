from django.http import HttpResponse
from django.shortcuts import render
from logging import getLogger

# Create your views here.

logger = getLogger(__name__)


def home(request):
    context = {'info': ['Всем привет!', 'И добро пожаловать!',
                        'Это локальный сайт,', 'для организации судейства в конкурсах', 'Оренбургского президентского кадетского училища']}
    logger.info('Главная страница')
    return render(request, 'app_main/index.html', context=context)


def base(request):
    logger.info('Базовый шаблон. Зачем сюда-то?')
    return render(request, 'base.html')


def about(request):
    logger.info("Загружена страница обо мне")
    context = {'title': 'Об авторе'}
    return render(request, 'app_main/about.html', context)


def contacts(request):
    logger.info("Загружена страница контактов")
    context = {'title': 'Контакты'}
    return render(request, 'app_main/contacts.html', context)
