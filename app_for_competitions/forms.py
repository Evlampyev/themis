from django import forms
import datetime
from .models import Competition
from app_for_judges.models import TableTask
from django.utils.translation import gettext_lazy as _


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition

        fields = ['name', 'fullname']

    date = forms.DateField(label=_("Дата"), initial=datetime.date.today,
                           widget=forms.DateInput(attrs={
                               'class': 'form-control',
                               'type' : 'date'  # теперь календарь
                           }))
    active = forms.BooleanField(label=_("Активно"), required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))

    def clean_date(self):
        """Проверка даты: не ранее сегодня"""
        my_date = self.cleaned_data['date']
        if datetime.date.today() > my_date:
            raise forms.ValidationError(u'Указана не верная дата! "%s"' % my_date)
        return my_date

class  TableTaskForm(forms.ModelForm):
    class Meta:
        model = TableTask
        fields = ['participant', 'time']

    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M:%S'))