# Generated by Django 5.0.1 on 2024-02-20 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_for_judges', '0008_tabletask_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_place', models.IntegerField()),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_for_judges.participant', verbose_name='Участник')),
            ],
            options={
                'verbose_name': 'Результат конкурса',
                'verbose_name_plural': 'Результаты конкурсов',
                'db_table': 'competition_results',
            },
        ),
    ]