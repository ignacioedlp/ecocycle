from django.shortcuts import render
from .forms import OrderForm
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
        assignVariableByTaskAndCase(token, session_id, case_id, 'dni', orden.dni, 'java.lang.String')
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
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():

            # Guardar directamente el formulario y obtener la orden
            orden = form.save()

            # Almacenar la orden en el decorador para uso posterior
            nueva_orden.orden = orden

            # Procesar la orden en Bonita
            procesar_bonita(request, orden)
            
            messages.success(request, 'La orden ha sido creada con éxito.')
        else:
            messages.error(request, 'Hubo un error al crear la orden. Por favor, verifica los datos.')
    else:
        form = OrderForm()

    return render(request, "nueva_orden.html", {"form": form})

def index(request):
    return render(request, "index.html")
