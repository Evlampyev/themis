from django import forms
from django.contrib.auth.models import User

from .models import Judge
from app_for_competitions.models import Competition
from django.utils.translation import gettext_lazy as _


class JudgeForm(forms.ModelForm):

    class Meta:
        model = Judge
        fields = ['patronymic', 'post', 'regalia', 'organization']


    last_name = forms.CharField(max_length=25, label=_("Фамилия"))
    first_name = forms.CharField(max_length=25, label=_("Имя"))
    patronymic = forms.CharField(empty_value="", label=_("Отчество"))
    post = forms.CharField(max_length=100, label=_("Должность"))
    regalia = forms.CharField(empty_value="", label=_("Заслуги и регалии"))
    organization = forms.CharField(max_length=100, label=_("Место работы"))
    status = forms.ChoiceField(choices=Judge.STATUSES, label=_("Статус на конкурсе"))
    competition = forms.ModelChoiceField(
        queryset=Competition.objects.all().order_by('name'), blank=True, label=_("Конкурс"))
    # is_active = forms.BooleanField(required=True)  # по умолчанию галочка на True

    field_order = ['last_name', 'first_name', 'patronymic', 'post', 'regalia', 'organization', 'status',
                           'competition'] # меняет порядок полей в форме
