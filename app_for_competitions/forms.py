from django import forms
import datetime
from .models import Competition
from app_for_judges.models import TableTask, Participant, CompetitionTask
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class CompetitionForm(forms.ModelForm):
    """
    Форма создания Конкурса
    """

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
        """Проверка даты Конкурса: не ранее сегодня"""
        my_date = self.cleaned_data['date']
        if datetime.date.today() > my_date:
            raise forms.ValidationError(u'Указана не верная дата! "%s"' % my_date)
        return my_date


class TableTaskForm(forms.ModelForm):
    """
    Форма судейства любого этапа конкурса
    """

    class Meta:
        model = TableTask
        exclude = ("result_place", "competition_task")  # исключая поле

    participant = forms.ModelChoiceField(
        queryset=Participant.objects.filter(competition__active=True).order_by('last_name'), label=_("Участник"))
    total_time = forms.TimeInput(format='%M:%S')

    # выбираются участники чей конкурс сейчас активен, по идее должны выбираться, кто на этот конкурс заявлен
    def clean_fields(self):
        time = self.cleaned_data['field_name']
        if time:
            raise ValidationError({'field_name': ["error message", ]})
        print(time)
        return time

    def clean_points(self):
        """Проверка поля сумма баллов"""
        data = self.cleaned_data['points']
        total = 0
        for i in range(4):  # 4 - количество полей промежуточных баллов
            try:
                temp = int(self.cleaned_data['intermediate_points_' + str(i + 1)])
            except TypeError:
                temp = 0
                # raise ArithmeticError('Нет таких данных')
            finally:
                total += temp
                # print(f"сумму балов подсчитали: {total}")

        if data != total and total != 0:
            print("Не соответствует сумма")
            raise ValidationError("Сумма баллов не равна сумме промежуточных данных")
        return data


class CompetitionTaskForm(forms.ModelForm):
    class Meta:
        model = CompetitionTask
        fields = ['name', 'judging', 'name_intermediate_points_1', 'name_intermediate_points_2',
                  'name_intermediate_points_3', 'name_intermediate_points_4', "name_points", "name_correction_score_up",
                  "name_correction_score_down", "name_intermediate_time_1", "name_intermediate_time_2",
                  "name_average_time", "name_total_time", "name_correction_time"]

    required_css_class = "form_field"
    not_required_css_class = "form_field"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Название этапа')
