# Generated by Django 5.0.1 on 2024-02-08 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_for_competitions', '0003_alter_competition_name'),
        ('app_for_judges', '0004_alter_participantsteam_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='competition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_for_competitions.competition', verbose_name='Соревнования'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_for_judges.participantsteam', verbose_name='Команда'),
        ),
        migrations.AlterField(
            model_name='participantsteam',
            name='competition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_for_competitions.competition', verbose_name='Соревнования'),
        ),
        migrations.CreateModel(
            name='TableTask',
            fields=[
                ('competition_task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app_for_competitions.competitiontask')),
                ('time', models.TimeField(verbose_name='Время')),
                ('result_place', models.IntegerField(default=0, verbose_name='_Очки')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_for_judges.participant')),
            ],
            options={
                'verbose_name': 'Таблица этапа',
                'verbose_name_plural': 'Таблицы этапов',
                'db_table': 'table_tasks',
            },
        ),
    ]