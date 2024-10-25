from django.shortcuts import render, redirect
from .forms import OrderForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .helpers.bonita_helpers import (
    authenticate, 
    getProcessId, 
    initProcess, 
    getTaskByCase, 
    assignVariableByTaskAndCase,
    getUserIdByUsername, 
    assignUserToTask, 
    completeTask
)
from django.http import JsonResponse
import requests
from django.conf import settings
from recolectores.api.views.auth_views import CustomTokenObtainPairView
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from recolectores.permissions import IsRecolector
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
import jwt
from recolectores.models import User

def procesar_bonita(token, recolector_id, material, cantidad, deposito):
        try:
            # 1. Me autentico en Bonita
            token_bonita, session_id = authenticate()

            # 2. Obtengo el ID del proceso de la orden
            process_id = getProcessId(token_bonita, session_id, 'Recoleccion')

            # 3. Instancio el proceso
            case_id = initProcess(token_bonita, session_id, process_id)

            # 5. Busco la actividad por caso
            task_id = getTaskByCase(token_bonita, session_id, case_id)

            # 6. Asigno las variables de la actividad
            assignVariableByTaskAndCase(token_bonita, session_id, case_id, 'recolector_id', recolector_id, 'java.lang.Integer')
            assignVariableByTaskAndCase(token_bonita, session_id, case_id, 'material', material.name, 'java.lang.String')
            assignVariableByTaskAndCase(token_bonita, session_id, case_id, 'material_id', material.id, 'java.lang.Integer')
            assignVariableByTaskAndCase(token_bonita, session_id, case_id, 'cantidad', int(cantidad), 'java.lang.Integer')
            assignVariableByTaskAndCase(token_bonita, session_id, case_id, 'deposito', deposito.name, 'java.lang.String')
            assignVariableByTaskAndCase(token_bonita, session_id, case_id, 'deposito_id', deposito.id, 'java.lang.Integer')
            assignVariableByTaskAndCase(token_bonita, session_id, case_id, 'token', token, 'java.lang.String')

            # 7. Obtengo el userId del usuario por username
            user_id = getUserIdByUsername(token_bonita, session_id)

            # 8. Asigno la actividad al usuario
            assignUserToTask(token_bonita, session_id, task_id, user_id)

            # 9. Completo la actividad asi avanza el proceso
            completeTask(token_bonita, session_id, task_id)

        except Exception as e:
            raise Exception(f"Error en el proceso de Bonita: {str(e)}")

@permission_classes([IsAuthenticated, IsRecolector])
def nueva_orden(request):
    try:
        token = request.session['jwt_token']
        decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        
        # Acceder a los datos del payload
        user_id = decoded_payload.get('user_id') 
        user = User.objects.get(id=user_id)

        if not user.groups.filter(name='Recolector').exists():
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('login')  # Redirige al login o a una página de acceso denegado

        if not token:
            return redirect('login')  # Redirige al login si no hay token

        api_url = f'{settings.API_URL}/api/v1/ordenes/'

        if request.method == "POST":        
            form = OrderForm(request.POST)
            if form.is_valid():
                
                procesar_bonita(token, user_id, form.cleaned_data['material'], form.cleaned_data['cantidad_inicial'], form.cleaned_data['deposito'])
            else:
                # Mostrar errores de validación del formulario
                messages.error(request, 'Error al crear la orden.')
        else:
            form = OrderForm()
        return render(request, "nueva_orden.html", {"form": form})
    except KeyError:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('login')  # Redirige al login o a una página de acceso denegado

def login(request):

    api_url = f'{settings.API_URL}/api/v1/login/'
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password'],
            }

            headers = {
                'Content-Type': 'application/json',
            }

            # Crear una petición simulada de Django Rest Framework
            factory = APIRequestFactory()
            api_request = factory.post('/api/v1/login/', data, format='json')

            # Simular una vista de DRF
            custom_view = CustomTokenObtainPairView.as_view()
            api_response = custom_view(api_request)

            if api_response.status_code == 200:
                # Autenticación exitosa, obtener el token JWT
                data = api_response.data
                token = data.get('access')
                # Guardar el token en la sesión
                request.session['jwt_token'] = token
                # Sesión iniciada con éxito
                messages.success(request, 'Inicio de sesión exitoso')
            else:
                # Mostrar errores si falla el inicio de sesión
                form.add_error(None, 'Los datos ingresados son incorrectos')
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def index(request):
    return render(request, "index.html")
