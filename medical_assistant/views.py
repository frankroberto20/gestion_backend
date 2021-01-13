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
            return JsonResponse(user.serialize(), safe=False, status=200)
        else:
            JsonResponse({"message": "Invalid username and/or password."}, status=400)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logout successful."}, status=200)

@csrf_exempt
@login_required
def patients(request):
    user = request.user
    if request.method == 'GET' and user.tipoUsuario.id == 1:
        return JsonResponse([paciente.serialize() for paciente in Paciente.objects.all()], safe=False)

    elif request.method == 'POST' and user.tipoUsuario.id == 1:
        data = json.loads(request.body)

        try:
            with transaction.atomic():
                if 'cedula' in data:
                    usuario = Usuario(
                        first_name = data['nombre'],
                        last_name = data['apellidos'],
                        FechaNacimiento = data['fecha_nacimiento'],
                        Cedula = data['cedula'],
                        Sexo = data['sexo'],
                        username = data['username'],
                        tipoUsuario = TipoUsuario.objects.get(id=3)
                    )
                    usuario.set_password(data['password'])
                    paciente = Paciente(
                        usuario = usuario
                    )
                else:
                    usuario = Usuario(
                        first_name = data['nombre'],
                        last_name = data['apellidos'],
                        FechaNacimiento = data['fecha_nacimiento'],
                        Sexo = data['sexo'],
                        username = data['username'],
                        password = data['password'],
                        tipoUsuario = TipoUsuario.objects.get(id=3)
                    )
                    
                    paciente = Paciente(
                        usuario = usuario,
                        NombreTutor = data['nombre_tutor'],
                        CedulaTutor = data['cedula_tutor']
                    )

                if 'enfermedad' in data:
                    for enfermedad in data['enfermedad']:
                        paciente.Enfermedades.add(Enfermedad.objects.get(pk=enfermedad))
                
                usuario.save()
                
                paciente.save()

            return JsonResponse({'message': 'Patient added succesfully.'}, status=200)

        except:
            return JsonResponse({'error': f'Error adding patient.'}, status=400)


@csrf_exempt
@login_required
def patient_by_id(request, id):
    if request.method == 'GET':
        try:
            paciente = Paciente.objects.get(id=id)
            return JsonResponse(paciente.serialize(), safe=False, status=200)
        except:
            return JsonResponse({'error': 'Patient not found'}, status=400)

    elif request.method == "DELETE":

        try:
            paciente = Paciente.objects.get(id= id)
            paciente.usuario.delete()
            return JsonResponse({'message' : 'Patient deleted successfully.'})
        except:        
            return JsonResponse({'error': "Patient not found"}, status = 400)


    elif request.method == "PATCH":
        data = json.loads(request.body)

        try:
            with transaction.atomic():
                paciente = Paciente.objects.get(id=id)
                
                if 'cedula' in data:
                    paciente.usuario.first_name = data['nombre']
                    paciente.usuario.last_name = data['apellidos']
                    paciente.usuario.FechaNacimiento = data['fecha_nacimiento']
                    paciente.usuario.Cedula = data['cedula']
                    paciente.usuario.Sexo = data['sexo']
                    paciente.usuario.username = data['username']
                else:
                    paciente.usuario.first_name = data['nombre']
                    paciente.usuario.last_name = data['apellidos']
                    paciente.usuario.FechaNacimiento = data['fecha_nacimiento']
                    paciente.usuario.Sexo = data['sexo']
                    paciente.usuario.username = data['username']

                    paciente.NombreTutor = data['nombre_tutor']
                    paciente.CedulaTutor = data['cedula_tutor']

                if 'enfermedad' in data:
                    for enfermedad in data['enfermedad']:
                        paciente.Enfermedades = Enfermedad.objects.get(NombreEnfermedad=enfermedad)

                paciente.usuario.save()
                paciente.save()
                
                return JsonResponse({'message': 'Patient modified succesfully.'}, status=200)
        except:
            return JsonResponse({'error': 'Patient not found'}, status=400)
         
@csrf_exempt
@login_required
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
            JsonResponse({'message': 'Disease added succesfully.', 'id': enfermedad.id}, status=200)
        
        except:
            JsonResponse({'error': 'Error in adding disease.'}, status=400)


@csrf_exempt
@login_required
def doctors(request):
    user = request.user
    if request.method == 'GET' and user.tipoUsuario.id == 1:
        return JsonResponse([doctor.serialize() for doctor in Doctor.objects.all()], safe=False)
    
    elif request.method == 'POST' and user.tipoUsuario.id == 1:
        data = json.loads(request.body)

        try:
            with transaction.atomic():
                usuario = Usuario(
                    first_name = data['nombre'],
                    last_name = data['apellidos'],
                    FechaNacimiento = data['fecha_nacimiento'],
                    Cedula = data['cedula'],
                    Sexo = data['sexo'],
                    username = data['username'],
                    tipoUsuario = TipoUsuario.objects.get(id=4)
                )
                usuario.set_password(data['password'])
                usuario.save()

                doctor = Doctor(
                    usuario = usuario,
                    especialidad = Especialidad.objects.get(pk=data['especialidad']),
                    subespecialidad = SubEspecialidad.objects.get(pk=data['sub_especialidad']),
                )
                doctor.save()
                return JsonResponse({'message': 'Doctor created succesfully.'}, status=200)
        
        except:
            return JsonResponse({'error': 'Error in creating doctor'}, status=400)


    

@csrf_exempt
@login_required
def doctor_by_id(request, id):
    user = request.user
    if request.method == 'GET':
        try:
            doctor = Doctor.objects.get(id=id)
            return JsonResponse(doctor.serialize(), safe=False, status=200)
        except:
            return JsonResponse({'error': 'Doctor not found'}, status=400)

    elif request.method == "DELETE":
        data = json.loads(request.body)
        
        try:
            doctor = Doctor.objects.get(id=id)
            doctor.usuario.delete()
            return JsonResponse({'message' : 'Doctor deleted successfully.'})
        except:        
            return JsonResponse({'error': "Doctor not found"}, status = 400)


    elif request.method == "PATCH":
        data = json.loads(request.body)

        try:
            with transaction.atomic():
                doctor = Doctor.objects.get(id=id)

                doctor.usuario.first_name = data['nombre']
                doctor.usuario.last_name = data['apellidos']
                doctor.usuario.FechaNacimiento = data['fecha_nacimiento']
                doctor.usuario.Cedula = data['cedula']
                doctor.usuario.Sexo = data['sexo']
                doctor.usuario.username = data['username']
                doctor.usuario.password = data['password']

                doctor.usuario.save()

                if 'especialidad' in data:
                    doctor.especialidad = Especialidad.objects.get(pk=data['especialidad'])
                elif 'especialidad' and 'sub_especialidad' in data:
                    doctor.especialidad = Especialidad.objects.get(pk=data['especialidad'])
                    doctor.subespecialidad = SubEspecialidad.objects.get(pk=data['sub_especialidad'])

                doctor.save()
                return JsonResponse({'message': 'Doctor modified succesfully.'}, status=200)
        except:
            return JsonResponse({'error': 'Doctor not found'}, status=400)


@csrf_exempt
@login_required
def specialties(request):
    if request.method == 'GET':
        return JsonResponse([especialidad.serialize() for especialidad in Especialidad.objects.all()], safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)

        try:
            especialidad = Especialidad(
                NombreEspecialidad = data['nombre_especialidad'],
            )
            especialidad.save()
            return JsonResponse({'message': 'Especialty created succesfully.', 'id': especialidad.id}, status=200)
        except:
            return JsonResponse({'error': 'Error in creating especialty'}, status=400)


    elif request.method == "DELETE":
        data = json.loads(request.body)
        
        try:
            specialty = Especialidad.objects.get(id=data['especialidad'])
            specialty.delete()
            return JsonResponse({'message' : 'Specialty deleted successfully.'})
        except:        
            return JsonResponse({'error': "Specialty not found"}, status = 400)


    elif request.method == "PATCH":
        data = json.loads(request.body)

        try:
            specialty = Especialidad.objects.get(id=data['especialidad'])

            specialty.NombreEspecialidad = data['nombre_especialidad']

            specialty.save()

            return JsonResponse({'message': 'Specialty modified succesfully.'}, status=200)
        except:
            return JsonResponse({'error': 'Specialty not found'}, status=400)    

@csrf_exempt
@login_required
def subspecialties(request):
    if request.method == 'GET':
        return JsonResponse([subespecialidad.serialize() for subespecialidad in SubEspecialidad.objects.all()], safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)

        try:
            subespecialidad = SubEspecialidad(
                NombreSubEspecialidad = data['nombre_subespecialidad'],
                especialidad = Especialidad.objects.get(pk=data['especialidad'])
            )
            subespecialidad.save()
            return JsonResponse({'message': 'Subespecialty created succesfully.', 'id': subespecialidad.id}, status=200)
        except:
            return JsonResponse({'error': 'Error in creating subespecialty'}, status=400)


    elif request.method == "DELETE":
        data = json.loads(request.body)
        
        try:
            subspecialty = SubEspecialidad.objects.get(id=data['subespecialidad'])
            subspecialty.delete()
            return JsonResponse({'message' : 'Subspecialty deleted successfully.'})
        except:        
            return JsonResponse({'error': "Subspecialty not found"}, status = 400)


    elif request.method == "PATCH":
        data = json.loads(request.body)

        try:
            subspecialty = SubEspecialidad.objects.get(id=data['subespecialidad'])

            subspecialty.NombreSubEspecialidad = data['nombre_subespecialidad']
            subspecialty.especialidad = Especialidad.objects.get(id=data['especialidad'])

            subspecialty.save()

            return JsonResponse({'message': 'Subspecialty modified succesfully.'}, status=200)
        except:
            return JsonResponse({'error': 'Subspecialty not found'}, status=400)  

@csrf_exempt
#@login_required
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


    elif request.method == "DELETE":
        data = json.loads(request.body)
        
        try:
            tipo_usuario = TipoUsuario.objects.get(id=data['id_tipousuario'])
            tipo_usuario.delete()
            return JsonResponse({'message' : 'UserType deleted successfully.'})
        except:        
            return JsonResponse({'error': "UserType not found"}, status = 400)


    elif request.method == "PATCH":
        data = json.loads(request.body)

        try:
            tipo_usuario = TipoUsuario.objects.get(id=data['id_tipousuario'])

            tipo_usuario.NombreTipoUsuario = data['nombre_tipousuario']

            tipo_usuario.save()

            return JsonResponse({'message': 'UserType modified succesfully.'}, status=200)
        except:
            return JsonResponse({'error': 'UserType not found'}, status=400) 

@csrf_exempt
@login_required
def checkups(request):
    user = request.user
    if request.method == 'GET':
        if user.tipoUsuario.id == 3 or user.tipoUsuario.id == 4:
            return JsonResponse([consulta.serialize() for consulta in user.consultas], safe=False, status=200)
        else:
            return JsonResponse([consulta.serialize() for consulta in Consulta.objects.all()], safe=False, status=200)
    if request.method == 'POST':
        if user.tipoUsuario.id == 4:
            data = json.loads(request.body)
        
            paciente = Paciente.objects.get(id=data['paciente'])
            doctor = user.doctor

            consulta = Consulta(
                paciente = paciente,
                doctor = doctor,
                Titulo = data['titulo'],
                Descripcion = data['descripcion'],
                Archivo = data['archivo']
            )

            consulta.save()
            return JsonResponse({'message': f'Checkup for {paciente.usuario.first_name} {paciente.usuario.last_name} created succesfully'}, status=200, safe=False)
        elif user.tipoUsuario.id == 2 or user.tipoUsuario.id == 1:
            data = json.loads(request.body)
        
            paciente = Paciente.objects.get(id=data['paciente'])
            doctor = Doctor.objects.get(id=data['doctor'])

            consulta = Consulta(
                paciente = paciente,
                doctor = doctor,
                Titulo = data['titulo'],
                Descripcion = data['descripcion'],
                Archivo = data['archivo']
            )

            consulta.save()
            return JsonResponse({f'Checkup for {paciente.usuario.first_name} {paciente.usuario.last_name} created succesfully'}, status=200, safe=False)
        else:
            return JsonResponse({'message': 'Permission denied.'}, status=401)

@csrf_exempt
@login_required
def checkups_patient(request, patient_id):
    user = request.user
    if request.method == 'GET' and user.tipoUsuario.id == 1:
        try:
            paciente = Paciente.objects.get(id=patient_id)
            #if paciente.consultas.count() == 0:
            #    return JsonResponse({'message': 'No checkups found'}, status=200)
            return JsonResponse([consulta.serialize() for consulta in Consulta.objects.filter(paciente = paciente)], safe=False, status=200)
        except:
            return JsonResponse({'error': 'Patient not found'}, status=404)
    elif request.method == 'POST' and user.tipoUsuario.id == 4:
        data = json.loads(request.body)
    
        paciente = Paciente.objects.get(id=patient_id)
        doctor = user.doctor

        consulta = Consulta(
            paciente = paciente,
            doctor = doctor,
            Titulo = data['titulo'],
            Descripcion = data['descripcion'],
            Fecha = data['fecha']
        )

        consulta.save()
        return JsonResponse({'message': f'Checkup for patient {paciente.usuario.first_name} {paciente.usuario.last_name} by doctor {doctor.usuario.first_name} {doctor.usuario.last_name} created succesfully'}, status=200)
    else:
        return JsonResponse({'message': 'Permission denied.'}, status=401)

@csrf_exempt
@login_required
def checkups_doctor(request, doctor_id):
    user = request.user
    if request.method == 'GET' and user.tipoUsuario.id == 1:
        try:
            doctor = Doctor.objects.get(id=doctor_id)
                #if paciente.consultas.count() == 0:
                #    return JsonResponse({'message': 'No checkups found'}, status=200)
            return JsonResponse([consulta.serialize() for consulta in Consulta.objects.filter(doctor = doctor)], safe=False, status=200)
        except:
            return JsonResponse({'error': 'Doctor not found'}, status=404)


@csrf_exempt
def search_patients(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        patient = Usuario.objects.filter(
            username__icontains=search_str) | Usuario.objects.filter(
            Cedula__icontains=search_str) | Usuario.objects.filter(
            tipoUsuario=3) 
        
        data = patient.values()
        return JsonResponse(list(data), safe=False)