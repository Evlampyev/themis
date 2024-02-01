from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from django.db import models

# Create your models here.


def get_name(self):
    """Переопределение метода __str__ для User"""
    return f' {self.last_name} {self.first_name}'

User.add_to_class("__str__", get_name)