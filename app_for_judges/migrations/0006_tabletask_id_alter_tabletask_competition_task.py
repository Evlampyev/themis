# Generated by Django 5.0.1 on 2024-02-08 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_for_competitions', '0003_alter_competition_name'),
        ('app_for_judges', '0005_alter_participant_competition_alter_participant_team_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabletask',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tabletask',
            name='competition_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_for_competitions.competitiontask'),
        ),
    ]