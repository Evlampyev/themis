from django.db import models
from django.utils.translation import gettext_lazy as _
from app_for_competitions.models import Competition  # не обращать внимание на красноту
import sys, os

sys.path.insert(0, os.path.abspath('..'))


# Create your models here.


class User(models.Model):
    class Meta:
        abstract = True  # данное поле указывает, что класс абстрактный
        # и что для него не нужно создавать таблицу

    name = models.CharField(_('Имя'), max_length=25)
    patronymic = models.CharField(_('Отчество'), max_length=25, default=None)
    last_name = models.CharField(_('Фамилия'), max_length=25)
    is_active = models.BooleanField(_('Активировать'), default=True)

    def __str__(self):
        return f"{self.last_name} {self.name}"


class Judge(User):
    STATUSES = (
        ('M', 'главный судья'),
        ('J', 'судья'),
        ('S', 'секретарь'),
        ('O', 'наблюдатель'),
    )

    class Meta:
        db_table = 'judges'
        verbose_name = _('Судьи')

    post = models.CharField(_('Занимаемая должность'), max_length=100)
    regalia = models.TextField(_('Заслуги и регалии'), default=None)
    organization = models.CharField(_('Место работы'), max_length=100)
    status = models.CharField(_('Статус на соревнованиях'), max_length=1,
                              choices=STATUSES, default='O')
    competitions = models.ManyToManyField(Competition, blank=True, default='Нет')

    def __str__(self):
        return f"{self.status}: {self.last_name} {self.name}. {self.patronymic}."

    def __eq__(self, other):
        return (self.name == other.name and self.patronymic == other.patronymic
                and self.last_name == other.last_name)
