import json
from django.contrib.auth.models import User
from django.db.models.expressions import F
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .models import *

# Create your views here.

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

        #try:
        usuario = Usuario(
            first_name = data['nombre'],
            last_name = data['apellidos'],
            FechaNacimiento = data['fecha_nacimiento'],
            Cedula = data['cedula'],
            Sexo = data['sexo'],
            username = "paciente" + data['cedula'],
        )

        usuario.save()

        paciente = Paciente(
            usuario = usuario,
            NombreTutor = data['nombre_tutor'],
            CedulaTutor = data['cedula_tutor']
        )

        if 'enfermedad' in data:
            for enfermedad in data['enfermedad']:
                paciente.enfermedades.add(Enfermedad.get(pk=enfermedad))

        paciente.save()
        return JsonResponse({'message': 'Patient added succesfully.'}, status=200)

        #except e:
            #return JsonResponse({'error': f'Error adding patient. {e}'}, status=400)

@csrf_exempt
def patient_by_id(request, id):
    if request.method == 'GET':
        paciente = Paciente.objects.get(pk=id)
        
            
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
        return JsonResponse([tipousuario.serialize() for tipousuario in TipoUsuario.objects.all()])
    elif request.method == 'POST':
        data = json.loads(request.body)

        try:
            especialidad = Especialidad(
                NombreTipoUsuario = data['nombre_tipousuario'],
            )
            especialidad.save()
            return JsonResponse({'message': 'User type created succesfully.'}, status=200)
        except:
            return JsonResponse({'error': 'Error in creating user type'}, status=400)

@csrf_exempt
def checkup(request):
    pass