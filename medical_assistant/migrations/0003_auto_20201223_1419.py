# Generated by Django 3.1 on 2020-12-23 18:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('medical_assistant', '0002_auto_20201223_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='TipoUsuario',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='FechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 23, 18, 19, 49, 230280, tzinfo=utc)),
        ),
    ]
