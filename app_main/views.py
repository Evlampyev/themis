from django.http import HttpResponse
from django.shortcuts import render
from logging import getLogger

# Create your views here.

logger = getLogger(__name__)


def index(request):
    context = {'info': ['Всем привет!', 'И добро пожаловать!']}
    logger.info('Главная страница')
    return render(request, 'app_main/index.html', context=context)


def base(request):
    logger.info('Базовый шаблон. Зачем сюда-то?')
    return render(request, 'base.html')


def about(request):
    logger.info("Загружена страница обо мне")

    return render(request, 'app_main/about.html')
