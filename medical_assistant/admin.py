from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(TipoUsuario)
admin.site.register(Usuario)
admin.site.register(Enfermedad)
admin.site.register(Paciente)
admin.site.register(Especialidad)
admin.site.register(SubEspecialidad)
admin.site.register(Doctor)
admin.site.register(Consulta)
