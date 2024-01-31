from django.core.management.base import BaseCommand
from appfirst.models import Competition


class Command(BaseCommand):
    help = "Добавление Соревнования/Конкурса"

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Короткое название')
        parser.add_argument('fullname', type=str, help='Полное наименование')

    def handle(self, *args, **kwargs):
        name = kwargs.get('name')
        fullname = kwargs.get('fullname')
        competition = Competition(name=name, fullname=fullname)
        competition.save()
        return f'Конкурс: "{name}" добавлен'
