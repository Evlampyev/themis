from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from app_for_competitions.models import Competition
from .models import Judge, Participant, ParticipantsTeam
from django.utils.translation import gettext_lazy as _


class JudgeEditForm(forms.ModelForm):
    class Meta:
        model = Judge
        fields = ['patronymic', 'post', 'regalia', 'organization']

    last_name = forms.CharField(max_length=25, label=_("Фамилия"))
    first_name = forms.CharField(max_length=25, label=_("Имя"))
    patronymic = forms.CharField(empty_value="", required=False, label=_("Отчество"))
    post = forms.CharField(max_length=100, label=_("Должность"))
    regalia = forms.CharField(empty_value="", required=False, label=_("Заслуги и регалии"))
    organization = forms.CharField(max_length=100, label=_("Место работы"))
    status = forms.ChoiceField(choices=Judge.STATUSES, label=_("Статус на конкурсе"))
    competition = forms.ModelChoiceField(
        queryset=Competition.objects.all().order_by('name'), blank=True, label=_("Конкурс"))
    # is_active = forms.BooleanField(required=True)  # по умолчанию галочка на True

    field_order = ['last_name', 'first_name', 'patronymic', 'post', 'regalia', 'organization', 'status',
                   'competition']  # меняет порядок полей в форме


class UserAddForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class JudgeAddForm(forms.ModelForm):
    class Meta:
        model = Judge
        fields = ('patronymic', 'post', 'regalia', 'organization', 'status', 'competitions')


class ParticipantAddForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'last_name', 'organization', 'birthday', 'competition', 'team']

    name = forms.CharField(max_length=25, label=_("Имя"))
    last_name = forms.CharField(max_length=25, label=_("Фамилия"))
    organization = forms.CharField(max_length=100, label=_("Образовательное учреждение"))
    birthday = forms.DateField(label=_("Дата рождения"))
    competition = forms.ModelChoiceField(
        queryset=Competition.objects.all().order_by('name'), blank=True, label=_("Конкурс"))
    team = forms.ModelChoiceField(
        queryset=ParticipantsTeam.objects.all().order_by('name'), blank=True, required=False, label=_("Команда"))

    required_css_class = "form_field"

    # non_required_css_class = "form_field"
