from django.core.management.base import BaseCommand
from app_for_judges.models import ParticipantsTeam



class Command(BaseCommand):
    help = "Добавление Команд - участников"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Количество команд')

    def handle(self, *args, **kwargs):
        count = kwargs.get('count')
        for i in range (1, count+1):
            name = f'Команда_{i}'
            organization = f'Организация_{i}'
            participant_team = ParticipantsTeam(name=name, organization=organization)
            participant_team.save()

        return f'{count} команд добавлены'
