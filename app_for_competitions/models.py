from django.db import models

from django.utils.translation import gettext_lazy as _


# Create your models here.


class Competition(models.Model):
    """Конкурсы"""

    class Meta:
        db_table = 'competitions'
        verbose_name = _('Конкурс')  # наименование в админке в единственном числе
        verbose_name_plural = _('Конкурсы')  # наименование в админке во множественном числе

    name = models.CharField(_('Сокращенное название'), max_length=50, unique=True)
    fullname = models.CharField(_('Полное наименование конкурса'), max_length=200,
                                default=None)
    date = models.DateField(_('Дата проведения'),
                            help_text="Дата начала")
    active = models.BooleanField(_('Активен'), default=True)

    def __str__(self):
        return self.name


class CompetitionTask(models.Model):
    """Этапы конкурса"""

    class Meta:
        db_table = 'competition_tasks'
        verbose_name = _('Этап конкурса')
        verbose_name_plural = _('Этапы конкурсов')

    name = models.CharField(max_length=50, verbose_name=_('Название этапа'))
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name=_('Конкурс'))
    judging = models.BooleanField(default=True, verbose_name=_('Возможность судейства'))

    name_intermediate_points_1 = models.CharField(max_length=20, default=None, blank=True,
                                                  verbose_name=_('Промежуточные баллы - 1'))
    name_intermediate_points_2 = models.CharField(max_length=20, default=None, blank=True,
                                                  verbose_name=_('Промежуточные баллы - 2'))
    name_intermediate_points_3 = models.CharField(max_length=20, default=None, blank=True,
                                                  verbose_name=_('Промежуточные баллы - 3'))
    name_intermediate_points_4 = models.CharField(max_length=20, default=None, blank=True,
                                                  verbose_name=_('Промежуточные баллы - 4'))
    name_points = models.CharField(max_length=20, default=None, blank=True, verbose_name=_('Сумма баллов')),
    name_correction_score_up = models.CharField(max_length=20, default=None, blank=True,
                                                verbose_name=_('Корректирующий балл, если больше'))
    name_correction_score_down = models.CharField(max_length=20, default=None, blank=True,
                                                  verbose_name=_('Корректирующий балл, если меньше'))
    name_intermediate_time_1 = models.CharField(max_length=20, default=None, blank=True,
                                                verbose_name=_('Промежуточное время - 1'))
    name_intermediate_time_2 = models.CharField(max_length=20, default=None, blank=True,
                                                verbose_name=_('Промежуточное время - 2'))
    name_average_time = models.CharField(max_length=20, default=None, blank=True, verbose_name=_('Среднее время'))
    name_total_time = models.CharField(max_length=20, default=None, blank=True, verbose_name=_('Время'))
    name_correction_time = models.CharField(max_length=20, default=None, blank=True,
                                            verbose_name=_('Корректирующее время'))

    def __str__(self):
        return f'Этап "{self.name}" конкурса "{self.competition}"'
