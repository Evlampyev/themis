from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Competition(models.Model):
    """Конкурсы"""

    class Meta:
        db_table = 'competitions'
        verbose_name = _('Конкурс') # наименование в админке в единственном числе
        verbose_name_plural = _('Конкурсы') # наименование в админке во множественном числе

    name = models.CharField(_('Сокращенное название'), max_length=50)
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

    name = models.CharField(max_length=50)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

