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
    pass



def delete_judge(request, pk):
    pass


def add_judge(request):
    pass


def edit_judge(request, pk):
   pass
