# Generated by Django 3.2.4 on 2022-09-28 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_changepassword'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChangePassword',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
