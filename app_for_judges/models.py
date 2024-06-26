from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import time
from django.utils.translation import gettext_lazy as _
from app_for_competitions.models import Competition, CompetitionTask
import sys
import os

sys.path.insert(0, os.path.abspath('..'))


# Create your models here.

class Judge(models.Model):
    """Судьи, привязанные к User"""
    STATUSES = (
        ('M', 'Главный судья'),
        ('J', 'Судья'),
        ('S', 'Секретарь'),
        ('O', 'Наблюдатель'),
    )

    class Meta:
        db_table = 'judges'
        verbose_name = _('Судья')
        verbose_name_plural = _('Судьи')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # связь Judge с User один к одному
    patronymic = models.CharField(_('Отчество'), max_length=25, null=True, blank=True, default=None)
    post = models.CharField(_('Занимаемая должность'), max_length=100,
                            default='Преподаватель ОД (математика, информатика и ИКТ)')
    regalia = models.TextField(_('Заслуги и регалии'), default='Преподаватель высшей категории')
    organization = models.CharField(_('Место работы'), max_length=100, default='Оренбургское ПКУ')
    status = models.CharField(_('Статус на соревнованиях'), max_length=1,
                              choices=STATUSES, default='O')
    competitions = models.ManyToManyField(Competition, blank=True, default='Нет')

    def __str__(self):
        last_name = User.objects.get(id=self.user_id).last_name
        first_name = User.objects.get(id=self.user_id).first_name
        patronymic = ''
        if self.patronymic is not None:
            patronymic = self.patronymic
        return f"{self.get_status_display()}: {last_name} {first_name} {patronymic}."


@receiver(post_save, sender=User)
def create_user_judge(sender, instance, created, **kwargs):
    """При создании User создаем Judge"""
    if created:
        Judge.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_judge(sender, instance, **kwargs):
    """При сохранении User сохраняем Judge"""
    instance.judge.save()


class Participant(models.Model):
    """Участники, НЕ привязанные к User"""

    objects = None

    class Meta:
        db_table = 'participants'
        verbose_name = _('Участник')
        verbose_name_plural = _('Участники')

    team = models.ForeignKey('ParticipantsTeam', on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name=_('Команда'))
    # models.SET_NULL: устанавливает NULL при удалении связанной строка из главной таблицы
    # models.SET_DEFAULT: устанавливает значение по умолчанию для внешнего ключа в зависимой таблице
    # team - может быть пустым
    name = models.CharField(_('Имя'), max_length=25)
    last_name = models.CharField(_('Фамилия'), max_length=25)
    organization = models.CharField(_('Образовательное учреждение'), max_length=100,
                                    default='ФГКОУ "Оренбургское ПКУ"')
    birthday = models.DateField(_('Дата рождения'))
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name=_('Соревнования'))

    def __str__(self):
        return f"{self.last_name} {self.name}"


class ParticipantsTeam(models.Model):
    """Участники - команды"""

    class Meta:
        db_table = 'participant_teams'
        verbose_name = _('Участник - команда')
        verbose_name_plural = _('Участники - команды')

    name = models.CharField(_('Название команды'), max_length=50, unique=True)
    organization = models.CharField(_('Образовательное учреждение'), max_length=100,
                                    default='ФГКОУ "Оренбургское ПКУ"')
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name=_('Соревнования'))

    def __str__(self):
        return f"{self.name}"


class TableTask(models.Model):
    """Общая таблица для судейства всех этапов соревнований"""

    class Meta:
        db_table = 'table_tasks'
        verbose_name = _('Таблица этапа')
        verbose_name_plural = _('Таблицы этапов')

    competition_task = models.ForeignKey(CompetitionTask, on_delete=models.CASCADE, verbose_name=_('Этап'))
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, verbose_name=_('Участник'))

    intermediate_points_1 = models.IntegerField(_('Промежуточные баллы - 1'), default=0, blank=True)
    intermediate_points_2 = models.IntegerField(_('Промежуточные баллы - 2'), default=0, blank=True)
    intermediate_points_3 = models.IntegerField(_('Промежуточные баллы - 3'), default=0, blank=True)
    intermediate_points_4 = models.IntegerField(_('Промежуточные баллы - 4'), default=0, blank=True)
    points = models.IntegerField(_('Сумма баллов'), default="", blank=True)
    correction_score_up = models.IntegerField(_('Корректирующий балл, если больше'), default=0, blank=True)
    correction_score_down = models.IntegerField(_('Корректирующий балл, если меньше'), default=0, blank=True)
    intermediate_time_1 = models.TimeField(_('Промежуточное время - 1, мм:сс'), default=time(minute=0, second=0),
                                           blank=True)
    intermediate_time_2 = models.TimeField(_('Промежуточное время - 2, мм:сс'), default=time(minute=0, second=0),
                                           blank=True)
    average_time = models.TimeField(_('Среднее время, мм:сс'), default=time(minute=0, second=0), blank=True)
    total_time = models.TimeField(_('Время, мм:сс'), default=time(minute=0, second=0), blank=True)
    correction_time = models.TimeField(_('Корректирующее время, мм:сс'), default=time(minute=0, second=0), blank=True)

    result_place = models.IntegerField(_('Место'), default=0, blank=True)

    def __str__(self):
        return f"{self.competition_task} {self.participant} {self.result_place}"


class CompetitionResult(models.Model):
    """Результаты конкурса"""

    class Meta:
        db_table = 'competition_results'
        verbose_name = _('Результат конкурса')
        verbose_name_plural = _('Результаты конкурсов')

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, verbose_name=_('Участник'))
    final_place = models.IntegerField(verbose_name=_('Сумма мест'))

    def __str__(self):
        return f'Участник: {self.participant} - сумма мест: {self.final_place}.'
