# Generated by Django 5.0.1 on 2024-02-03 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_for_judges', '0002_alter_judge_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParticipantsTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название команды')),
                ('organization', models.CharField(default='ФГКОУ "Оренбургское ПКУ"', max_length=100, verbose_name='Образовательное учреждение')),
            ],
            options={
                'verbose_name': 'Участник - команда',
                'verbose_name_plural': 'Участники - команды',
                'db_table': 'participants_team',
            },
        ),
        migrations.AlterModelOptions(
            name='judge',
            options={'verbose_name': 'Судья', 'verbose_name_plural': 'Судьи'},
        ),
        migrations.AlterField(
            model_name='judge',
            name='post',
            field=models.CharField(default='Преподаватель ОД (математика, информатика и ИКТ)', max_length=100, verbose_name='Занимаемая должность'),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=25, verbose_name='Фамилия')),
                ('organization', models.CharField(default='ФГКОУ "Оренбургское ПКУ"', max_length=100, verbose_name='Образовательное учреждение')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_for_judges.participantsteam')),
            ],
            options={
                'verbose_name': 'Участник',
                'verbose_name_plural': 'Участники',
                'db_table': 'participants',
            },
        ),
    ]
