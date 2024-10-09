from django.shortcuts import render, redirect
from .forms import OrderForm, LoginForm
from django.contrib import messages
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


def procesar_bonita(request, orden):
    try:
        # 1. Me autentico en Bonita
        token, session_id = authenticate()

        # 2. Obtengo el ID del proceso de la orden
        process_id = getProcessId(token, session_id, 'Recoleccion')

        # 3. Instancio el proceso 
        case_id = initProcess(token, session_id, process_id)

        # 4. Agrego a la orden el caseId del proceso
        orden.case_bonita_id = case_id
        orden.save()

        # 5. Busco la actividad por caso
        task_id = getTaskByCase(token, session_id, case_id)

        # 6. Asigno las variables de la actividad
        assignVariableByTaskAndCase(token, session_id, case_id, 'recolector_id', orden.recolector.id, 'java.lang.String')
        assignVariableByTaskAndCase(token, session_id, case_id, 'material_id', orden.material.id, 'java.lang.Integer')
        assignVariableByTaskAndCase(token, session_id, case_id, 'material', orden.material.name, 'java.lang.String')
        assignVariableByTaskAndCase(token, session_id, case_id, 'cantidad', orden.cantidad_inicial, 'java.lang.Integer')
        assignVariableByTaskAndCase(token, session_id, case_id, 'deposito', orden.deposito.name, 'java.lang.String')
        assignVariableByTaskAndCase(token, session_id, case_id, 'orden_id', orden.id, 'java.lang.Integer')

        # 7. Obtengo el userId del usuario por username
        user_id = getUserIdByUsername(token, session_id)

        # 8. Asigno la actividad al usuario
        assignUserToTask(token, session_id, task_id, user_id)

        # 9. Completo la actividad asi avanza el proceso
        completeTask(token, session_id, task_id)

    except Exception as e:
        # En caso de cualquier error, agregamos un mensaje de error
        messages.error(request, f"Error en el proceso de Bonita: {str(e)}")

def nueva_orden(request):
    token = request.session.get('token')  # Recuperar el JWT de la sesión

    if not token:
        return redirect('login')  # Redirige al login si no hay token
    
    api_url = f'{settings.API_URL}/api/v1/ordenes/'

    if request.method == "POST":        
        form = OrderForm(request.POST)
        if form.is_valid():

            data = {
                'material': form.cleaned_data['material'],
                'deposito': form.cleaned_data['deposito'],
                'cantidad_inicial': form.cleaned_data['cantidad_inicial'],
                'cantidad_final': form.cleaned_data.get('cantidad_final', None)
            }

            headers = {
                'Authorization': f'Bearer {token}',  # Incluimos el JWT en las cabeceras
                'Content-Type': 'application/json',
            }

            # Enviar la petición POST para crear la orden
            response = requests.post(api_url, json=data, headers=headers)

            if response.status_code == 201:
                # Orden creada con éxito, redirigir o mostrar mensaje de éxito
                messages.success(request, 'La orden ha sido creada con éxito, su # de orden es: ' + str(response.json()['id']))
            else:
                # Mostrar errores si la creación falla
                form.add_error(None, 'Error al crear la orden.')
        else:
            # Mostrar errores de validación del formulario
            messages.error(request, 'Error al crear la orden.')
    else:
        form = OrderForm()

    return render(request, "nueva_orden.html", {"form": form})

def index(request):
    return render(request, "index.html")
