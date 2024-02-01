from django.utils.translation import gettext_lazy as _
from app_for_competitions.models import Competition  # не обращать внимание на красноту
import sys, os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
        verbose_name = _('Судьи')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # связь Judge с User один к одному
    patronymic = models.CharField(_('Отчество'), max_length=25, null=True, blank=True, default=None)
    post = models.CharField(_('Занимаемая должность'), max_length=100, default='Преподаватель ОД (математика, информатика и ИКТ')
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


