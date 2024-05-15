from django import forms
import datetime
from .models import Competition
from app_for_judges.models import TableTask, Participant, CompetitionTask
from django.utils.translation import gettext_lazy as _


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'fullname']

    date = forms.DateField(label=_("Дата"), initial=datetime.date.today,
                           widget=forms.DateInput(attrs={
                               'class': 'form-control',
                               'type': 'date'  # теперь календарь
                           }))
    active = forms.BooleanField(label=_("Активно"), required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))

    def clean_date(self):
        """Проверка даты: не ранее сегодня"""
        my_date = self.cleaned_data['date']
        if datetime.date.today() > my_date:
            raise forms.ValidationError(u'Указана не верная дата! "%s"' % my_date)
        return my_date


class TableTaskForm(forms.ModelForm):
    class Meta:
        model = TableTask
        fields = ['participant', 'time']

    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M:%S'), label=_("Время"))
    participant = forms.ModelChoiceField(
        queryset=Participant.objects.filter(competition__active=True).order_by('last_name'), label=_("Участник"))
    # выбираются участники чей конкурс сейчас активен, по идее должны выбираться, кто на этот конкурс заявлен


class CompetitionTaskForm(forms.ModelForm):
    class Meta:
        model = CompetitionTask
        fields = ['name', 'judging', 'name_intermediate_points_1', 'name_intermediate_points_2',
                  'name_intermediate_points_3', 'name_intermediate_points_4', "name_points", "name_correction_score_up",
                  "name_correction_score_down", "name_intermediate_time_1", "name_intermediate_time_1",
                  "name_average_time", "name_total_time", "name_correction_time" ]


    required_css_class = "form_field"
    not_required_css_class = "form_field"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Название этапа')
