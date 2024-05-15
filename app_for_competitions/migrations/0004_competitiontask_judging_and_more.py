# Generated by Django 5.0.1 on 2024-05-15 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_for_competitions', '0003_alter_competition_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitiontask',
            name='judging',
            field=models.BooleanField(default=True, verbose_name='Возможность судейства'),
        ),
        migrations.AddField(
            model_name='competitiontask',
            name='name_average_time',
            field=models.CharField(default=None, max_length=20, verbose_name='Среднее время'),
        ),
        migrations.AddField(
            model_name='competitiontask',
            name='name_correction_score_down',
            field=models.CharField(default=None, max_length=20, verbose_name='Корректирующий балл, если меньше'),
        ),
        migrations.AddField(
            model_name='competitiontask',
            name='name_correction_score_up',
            field=models.CharField(default=None, max_length=20, verbose_name='Корректирующий балл, если больше'),
        ),
        migrations.AddField(
            model_name='competitiontask',
            name='name_correction_time',
            field=models.CharField(default=None, max_length=20, verbose_name='Корректирующее время'),
        ),
        migrations.AddField(
            model_name='competitiontask',
            name='name_intermediate_points_1',
            field=models.CharField(default=None, max_length=20, verbose_name='Промежуточные баллы - 1'),
        ),
        migrations.AddField(
            model_name='competitiontask',
            name='name_intermediate_points_2',
            field=models.CharField(default=None, max_length=20, verbose_name='Промежуточные баллы - 2'),
        ),
        migrations.AddField(
            model_name='competitiontask',
            name='name_intermediate_points_3',
            field=models.CharField(default=None, max_length=20, verbose_name='Промежуточные баллы - 3'),
        ),
        migrations.AddField(
            model_name='competitiontask',
            name='name_intermediate_points_4',
            field=models.CharField(default=None, max_length=20, verbose_name='Промежуточные баллы - 4'),
        ),
        migrations.AddField(
            model_name='competitiontask',
            name='name_intermediate_time_1',
            field=models.CharField(default=None, max_length=20, verbose_name='Промежуточное время - 1'),
        ),
        migrations.AddField(
            model_name='competitiontask',
            name='name_intermediate_time_2',
            field=models.CharField(default=None, max_length=20, verbose_name='Промежуточное время - 2'),
        ),
        migrations.AddField(
            model_name='competitiontask',
            name='name_points',
            field=models.CharField(default=None, max_length=20, verbose_name='Сумма баллов'),
        ),
        migrations.AddField(
            model_name='competitiontask',
            name='name_total_time',
            field=models.CharField(default=None, max_length=20, verbose_name='Время'),
        ),
        migrations.AlterField(
            model_name='competitiontask',
            name='competition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_for_competitions.competition', verbose_name='Конкурс'),
        ),
        migrations.AlterField(
            model_name='competitiontask',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название этапа'),
        ),
    ]
