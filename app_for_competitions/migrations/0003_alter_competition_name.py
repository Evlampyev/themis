# Generated by Django 5.0.1 on 2024-02-03 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_for_competitions', '0002_alter_competition_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Сокращенное название'),
        ),
    ]
