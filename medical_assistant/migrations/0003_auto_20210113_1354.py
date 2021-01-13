# Generated by Django 3.1 on 2021-01-13 17:54

import cloudinary.models
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('medical_assistant', '0002_auto_20210113_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consulta',
            name='Archivo',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='Archivo'),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='Fecha',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 13, 13, 54, 40, 122220)),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='FechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 13, 17, 54, 40, 118220, tzinfo=utc)),
        ),
    ]
