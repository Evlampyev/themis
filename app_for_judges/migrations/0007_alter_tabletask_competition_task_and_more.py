# Generated by Django 5.0.1 on 2024-02-08 18:30

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_for_competitions', '0003_alter_competition_name'),
        ('app_for_judges', '0006_tabletask_id_alter_tabletask_competition_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tabletask',
            name='competition_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_for_competitions.competitiontask', verbose_name='Этап'),
        ),
        migrations.AlterField(
            model_name='tabletask',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_for_judges.participant', verbose_name='Участник'),
        ),
        migrations.AlterField(
            model_name='tabletask',
            name='result_place',
            field=models.IntegerField(default=0, verbose_name='Место'),
        ),
        migrations.AlterField(
            model_name='tabletask',
            name='time',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name='Время, мм:сс'),
        ),
    ]
