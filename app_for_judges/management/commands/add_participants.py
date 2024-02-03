from django.core.management.base import BaseCommand
from random import randint
from datetime import date
from app_for_judges.models import Participant



class Command(BaseCommand):
    help = "Добавление Участников"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Количество участников')

    def handle(self, *args, **kwargs):
        count = kwargs.get('count')
        for i in range (1, count+1):
            name = f'Имя_{i}'
            last_name = f'Фамилия_{i}'
            organization = f'Организация_{i}'
            birthday = date(randint(2007, 2011), randint(1, 12), randint(1, 28))
            participant = Participant(name=name, last_name=last_name, organization=organization, birthday=birthday)
            participant.save()

        return f'{count} участников добавлены'
