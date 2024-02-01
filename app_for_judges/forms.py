from django import forms
import datetime
from .models import Judge
from app_for_competitions.models import Competition
from django.utils.translation import gettext_lazy as _


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = Judge
#
#         fields = ['name', 'patronymic', 'last_name', 'post', 'regalia', 'organization']
#
#     # name = forms.CharField(max_length=25)
#     # patronymic = forms.CharField(empty_value="")
#     # last_name = forms.CharField(max_length=25)
#     # post = forms.CharField(max_length=100)
#     # regalia = forms.CharField(empty_value="")
#     # organization = forms.CharField(max_length=100)
#     status = forms.ChoiceField(choices=Judge.STATUSES)
#     competition = forms.ModelChoiceField(
#         queryset=Competition.objects.all().order_by('name'), blank=True)
#     # is_active = forms.BooleanField(required=True)  # по умолчанию галочка на True
