from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from django.urls import reverse, reverse_lazy

from .forms import LoginUserForm


# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}


def logout_view(request):
    logout(request)
    return redirect('about')  # на главную страницу сайта
