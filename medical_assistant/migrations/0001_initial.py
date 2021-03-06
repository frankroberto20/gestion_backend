# Generated by Django 3.1 on 2021-01-13 16:46

import cloudinary.models
import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('Sexo', models.CharField(max_length=10)),
                ('FechaNacimiento', models.DateField(default=datetime.date(2021, 1, 13))),
                ('Cedula', models.CharField(blank=True, max_length=11, validators=[django.core.validators.RegexValidator(code='nomatch', message='Length has to be 11', regex='^.{11}$')])),
                ('FechaRegistro', models.DateTimeField(default=datetime.datetime(2021, 1, 13, 16, 46, 29, 567319, tzinfo=utc))),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Enfermedad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NombreEnfermedad', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NombreEspecialidad', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NombreTipoUsuario', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SubEspecialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NombreSubEspecialidad', models.CharField(max_length=100)),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subespecialidades', to='medical_assistant.especialidad')),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NombreTutor', models.CharField(blank=True, max_length=100)),
                ('CedulaTutor', models.CharField(blank=True, max_length=11, validators=[django.core.validators.RegexValidator(code='nomatch', message='Length has to be 11', regex='^.{11}$')])),
                ('Enfermedades', models.ManyToManyField(to='medical_assistant.Enfermedad')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relacion', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical_assistant.especialidad')),
                ('subespecialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical_assistant.subespecialidad')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titulo', models.CharField(max_length=100)),
                ('Descripcion', models.TextField()),
                ('Fecha', models.DateTimeField(default=datetime.datetime(2021, 1, 13, 12, 46, 29, 570818))),
                ('Archivo', cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='archivo')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultas', to='medical_assistant.doctor')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultas', to='medical_assistant.paciente')),
            ],
        ),
        migrations.AddField(
            model_name='usuario',
            name='tipoUsuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='medical_assistant.tipousuario'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
