# Generated by Django 3.2.4 on 2022-10-22 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.IntegerField(default=1, verbose_name='Количество'),
        ),
    ]
