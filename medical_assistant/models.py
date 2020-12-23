import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateField
from django.core.validators import RegexValidator
from django.db.models.fields.related import ForeignKey

# Create your models here.

class TipoUsuario(models.Model):
    NombreTipoUsuario = models.CharField(max_length=50)

    #Returns in JSON format
    def serialize(self):
        return {
            'nombre': self.NombreTipoUsuario
        }

class Usuario(AbstractUser):
    tipoUsuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, default=1)
    Sexo = models.CharField(max_length = 10)
    FechaNacimiento = models.DateField(default=datetime.date.today())
    Cedula = models.CharField(max_length=11, validators=[RegexValidator(regex='^.{11}$', message='Length has to be 11', code='nomatch')])
    FechaRegistro = models.DateTimeField(default=timezone.now())

class Enfermedad(models.Model):
    NombreEnfermedad = models.CharField(max_length=100)

class Paciente(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete= models.CASCADE)
    NombreTutor = models.CharField(max_length=100)
    CedulaTutor = models.CharField(max_length=11, validators=[RegexValidator(regex='^.{11}$', message='Length has to be 11', code='nomatch')])
    Enfermedades = models.ManyToManyField(Enfermedad)

class Especialidad(models.Model):
    NombreEspecialidad = models.CharField(max_length=100)

class SubEspecialidad(models.Model):
    especialidad = models.ForeignKey(Especialidad, on_delete= models.CASCADE, related_name='subespecialidades')
    NombreSubEspecialidad = models.CharField(max_length=100)

class Doctor(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    subespecialidad = models.ForeignKey(SubEspecialidad, on_delete = models.CASCADE)

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='consultas')
    Titulo = models.CharField(max_length = 100)
    Descripcion = models.TextField()
    Fecha = models.DateTimeField()


