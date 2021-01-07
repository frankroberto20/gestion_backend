import json
from django.contrib.auth.models import User
from django.db.models.expressions import F
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from .models import *

# Create your views here.

@csrf_exempt
def index(request):
    return JsonResponse({'message': 'Hello'})

@csrf_exempt
def login_view(request):
    if request.method == "POST":

        data = json.loads(request.body)

        # Attempt to sign user in
        #username = request.POST["username"]
        #password = request.POST["password"]

        username = data['username']
        password = data['password']

        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            JsonResponse({"message": "Invalid username and/or password."}, status=400)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logout successful."}, status=200)

@csrf_exempt
def patients(request):
    if request.method == 'GET':
        return JsonResponse([paciente.serialize() for paciente in Paciente.objects.all()], safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)

        try:
            with transaction.atomic():
                usuario = Usuario(
                    first_name = data['nombre'],
                    last_name = data['apellidos'],
                    FechaNacimiento = data['fecha_nacimiento'],
                    Cedula = data['cedula'],
                    Sexo = data['sexo'],
                    username = "paciente" + data['cedula'],
                    tipoUsuario = TipoUsuario.objects.get(id=3)
                )

                usuario.save()

                if 'nombre_tutor' and 'cedula_tutor' in data:
                    paciente = Paciente(
                    usuario = usuario,
                    NombreTutor = data['nombre_tutor'],
                    CedulaTutor = data['cedula_tutor']
                    )
                else:
                    paciente = Paciente(
                    usuario = usuario
                )
                
                paciente.save()

                if 'enfermedad' in data:
                    for enfermedad in data['enfermedad']:
                        paciente.Enfermedades.add(Enfermedad.objects.get(pk=enfermedad))

            return JsonResponse({'message': 'Patient added succesfully.'}, status=200)

        except:
            return JsonResponse({'error': f'Error adding patient.'}, status=400)

    elif request.method == "DELETE":
        data = json.loads(request.body)

        usuario = Usuario.objects.get(id=data['id'])

        if(usuario.tipoUsuario == TipoUsuario.objects.get(id=2)):
            usuario.delete()
            return JsonResponse({'message' : 'Patient deleted successfully.'})
        
        return JsonResponse({'message': "The patient doesn't exist"})

    elif request.method == "PATCH":
        data = json.loads(request.body)

        usuario = Usuario.objects.get(id=data['usuario_id'])

        usuario.first_name = data['nombre']
        usuario.last_name = data['apellidos']
        usuario.FechaNacimiento = data['fecha_nacimiento']
        usuario.Cedula = data['cedula']
        usuario.Sexo = data['sexo']
        usuario.username = "paciente" + data['cedula']

        usuario.save()

        if 'nombre_tutor' and 'cedula_tutor' in data:
            paciente = Paciente(
            usuario = usuario,
            NombreTutor = data['nombre_tutor'],
            CedulaTutor = data['cedula_tutor']
            )
        else:
            paciente = Paciente(
            usuario = usuario
        )

        if 'enfermedad' in data:
            for enfermedad in data['enfermedad']:
                #paciente.enfermedades.add(Enfermedad.get(pk=enfermedad))
                paciente.Enfermedades = Enfermedad.objects.get(NombreEnfermedad=enfermedad)

        paciente.save()
        return JsonResponse({'message': 'Patient modified succesfully.'}, status=200)


@csrf_exempt
def patient_by_id(request, id):
    if request.method == 'GET':
        try:
            paciente = Paciente.objects.get(pk=id)
            return JsonResponse(paciente.serialize(), safe=False, status=200)
        except:
            return JsonResponse({'error': 'Patient not found'}, status=400)
         
@csrf_exempt
def diseases(request):
    if request.method == 'GET':
        return JsonResponse([enfermedad.serialize() for enfermedad in Enfermedad.objects.all()], safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)

        try:
            enfermedad = Enfermedad(
                NombreEnfermedad = data['nombre_enfermedad']
            )
            enfermedad.save()
            JsonResponse({'message': 'Disease added succesfully.'}, status=200)
        
        except:
            JsonResponse({'error': 'Error in adding disease.'}, status=400)

@csrf_exempt
def doctors(request):
    if request.method == 'GET':
        return JsonResponse([doctor.serialize() for doctor in Doctor.objects.all()], safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)

        try:
            usuario = Usuario(
                Nombre = data['nombre'],
                Apellido = data['apellido'],
                FechaNacimiento = data['fecha_nacimiento'],
                Cedula = data['cedula'],
            )
            usuario.save()

            doctor = Doctor(
                usuario = usuario,
                especialidad = Especialidad.objects.get(pk=data['especialidad']),
                subespecialidad = SubEspecialidad.objects.get(pk=data['subespecialidad']),
            )
            doctor.save()
            return JsonResponse({'message': 'Doctor created succesfully.'}, status=200)
        
        except:
            return JsonResponse({'error': 'Error in creating doctor'}, status=400)

@csrf_exempt
def specialties(request):
    if request.method == 'GET':
        return JsonResponse([especialidad.serialize() for especialidad in Especialidad.objects.all()])
    elif request.method == 'POST':
        data = json.loads(request.body)

        try:
            especialidad = Especialidad(
                NombreEspecialidad = data['nombre_especialidad'],
            )
            especialidad.save()
            return JsonResponse({'message': 'Especialty created succesfully.'}, status=200)
        except:
            return JsonResponse({'error': 'Error in creating especialty'}, status=400)

@csrf_exempt
def subspecialties(request):
    if request.method == 'GET':
        return JsonResponse([subespecialidad.serialize() for subespecialidad in SubEspecialidad.objects.all()])
    elif request.method == 'POST':
        data = json.loads(request.body)

        try:
            subespecialidad = SubEspecialidad(
                NombreSubEspecialidad = data['nombre_subespecialidad'],
                especialidad = Especialidad.objects.get(pk=data['especialidad'])
            )
            subespecialidad.save()
            return JsonResponse({'message': 'Subespecialty created succesfully.'}, status=200)
        except:
            return JsonResponse({'error': 'Error in creating subespecialty'}, status=400)

@csrf_exempt
def usertypes(request):
    if request.method == 'GET':
        return JsonResponse([tipousuario.serialize() for tipousuario in TipoUsuario.objects.all()], safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)

        try:
            tipo_usuario = TipoUsuario(
                NombreTipoUsuario = data['nombre_tipousuario'],
            )
            tipo_usuario.save()
            return JsonResponse({'message': 'User type created succesfully.'}, status=200)
        except:
            return JsonResponse({'error': 'Error in creating user type'}, status=404)

@csrf_exempt
@login_required
def checkups(request):
    user = request.user
    if request.method == 'GET':
        if user.tipoUsuario.id == 3 or user.tipoUsuario.id == 4:
            return JsonResponse([consulta.serialize() for consulta in user.consultas], safe=False, status=200)
        else:
            return JsonResponse([consulta.serialize() for consulta in Consulta.objects.all()])
    if request.method == 'POST':
        if user.tipoUsuario.id == 4:
            data = json.loads(request.body)
        
            paciente = Paciente.objects.get(id=data['paciente'])
            doctor = user

            consulta = Consulta(
                paciente = paciente,
                doctor = doctor,
                Titulo = data['titulo'],
                Descripcion = data['descripcion'],
                Fecha = data['fecha']
            )

            consulta.save()
            return JsonResponse({f'Checkup for {paciente.usuario.first_name} {paciente.usuario.last_name} created succesfully'}, status=200)
        else:
            return JsonResponse([consulta.serialize() for consulta in Consulta.objects.all()])

@csrf_exempt
@login_required
def checkups_patient(request, patient_id):
    user = request.user
    if request.method == 'GET' and user.tipoUsuario.id == 1:
        try:
            paciente = Paciente.objects.get(id=patient_id)
            #if paciente.consultas.count() == 0:
            #    return JsonResponse({'message': 'No checkups found'}, status=200)
            return JsonResponse([consulta.serialize() for consulta in paciente.consultas], safe=False, status=200)
        except:
            return JsonResponse({'error': 'Patient not found'}, status=404)

@csrf_exempt
@login_required
def checkups_doctor(request, doctor_id):
    user = request.user
    if request.method == 'GET' and user.tipoUsuario.id == 1:
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            #if paciente.consultas.count() == 0:
            #    return JsonResponse({'message': 'No checkups found'}, status=200)
            return JsonResponse([consulta.serialize() for consulta in doctor.consultas], safe=False, status=200)
        except:
            return JsonResponse({'error': 'Doctor not found'}, status=404)

