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

    def __str__(self):
        return f"{self.id}: {self.NombreTipoUsuario}"

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

    def __str__(self):
        return f"{self.id}: {self.first_name}"

    def serialize(self):
        return {
            'id': self.id,
            'usuario': self.username,
            #'id_usuario_relacionado': self.relacion.id,
            'tipo_usuario': self.tipoUsuario.id,
            'nombre': self.first_name,
            'apellidos': self.last_name,
            'sexo': self.Sexo,
            'fecha_nacimiento': self.FechaNacimiento.strftime(f'%Y/%m/%d'),
            'cedula': self.Cedula
        }

class Enfermedad(models.Model):
    NombreEnfermedad = models.CharField(max_length=100)

    def serialize(self):
        return {
            'id': self.id,
            'nombre_enfermedad': self.NombreEnfermedad
        }

class Paciente(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete= models.CASCADE, related_name='relacion')
    NombreTutor = models.CharField(max_length=100, blank= True)
    CedulaTutor = models.CharField(max_length=11, validators=[RegexValidator(regex='^.{11}$', message='Length has to be 11', code='nomatch')], blank=True)
    Enfermedades = models.ManyToManyField(Enfermedad)

    def serialize(self):
        return {
            'id': self.id,
            'tipo_usuario': self.usuario.tipoUsuario.id,
            'nombre': self.usuario.first_name,
            'apellidos': self.usuario.last_name,
            'sexo': self.usuario.Sexo,
            'fecha_nacimiento': self.usuario.FechaNacimiento,
            'cedula': self.usuario.Cedula,
            'nombre_tutor': self.NombreTutor,
            'cedula_tutor': self.CedulaTutor,
            'enfermedades': [enfermedad.serialize() for enfermedad in self.Enfermedades.all()]
        }

class Especialidad(models.Model):
    NombreEspecialidad = models.CharField(max_length=100)

    def serialize(self):
        return {
            'id': self.id,
            'nombre_especialidad': self.NombreEspecialidad
        }

class SubEspecialidad(models.Model):
    especialidad = models.ForeignKey(Especialidad, on_delete= models.CASCADE, related_name='subespecialidades')
    NombreSubEspecialidad = models.CharField(max_length=100)

    def serialize(self):
        return {
            'id': self.id,
            'especialidad': self.especialidad.id,
            'nombre_sub_especialidad': self.NombreSubEspecialidad
        }

class Doctor(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    subespecialidad = models.ForeignKey(SubEspecialidad, on_delete = models.CASCADE)

    def serialize(self):
        return {
            'id': self.id,
            'tipo_usuario': self.usuario.tipoUsuario.id,
            'nombre': self.usuario.first_name,
            'apellidos': self.usuario.last_name,
            'sexo': self.usuario.Sexo,
            'fecha_nacimiento': self.usuario.FechaNacimiento,
            'cedula': self.usuario.Cedula,
            'especialidad': self.especialidad.id,
            'sub_especialidad': self.subespecialidad.id
        }

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='consultas')
    Titulo = models.CharField(max_length = 100)
    Descripcion = models.TextField()
    Fecha = models.DateTimeField(default=datetime.datetime.now())
    Archivo = models.FileField(upload_to='consultas', blank=True)

    def serialize(self):
        return {
            'id': self.id,
            'paciente': f'{self.paciente.usuario.first_name} {self.paciente.usuario.last_name}',
            'doctor': f'{self.doctor.usuario.first_name} {self.doctor.usuario.last_name}',
            'titulo': self.Titulo,
            'descripcion': self.Descripcion,
            'fecha': self.Fecha,
            'archivo': self.Archivo.url
        }


