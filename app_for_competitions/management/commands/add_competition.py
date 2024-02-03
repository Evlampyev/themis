from django.core.management.base import BaseCommand
from app_for_competitions.models import Competition
from datetime import datetime

class Command(BaseCommand):
    help = "Добавление Соревнования/Конкурса"

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Короткое название')
        parser.add_argument('fullname', type=str, help='Полное наименование')

    def handle(self, *args, **kwargs):
        name = kwargs.get('name')
        fullname = kwargs.get('fullname')
        competition = Competition(name=name, fullname=fullname, date=datetime.now())
        competition.save()
        return f'Конкурс: "{name}" добавлен'
