from rest_framework import viewsets, status
from recolectores.models import Orden
from recolectores.api.serializers import OrdenCreateSerializer, OrdenListSerializer, OrdenUpdateSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from recolectores.helpers.bonita_helpers import (
    authenticate, getProcessId, initProcess, getTaskByCase, 
    assignVariableByTaskAndCase, getUserIdByUsername, assignUserToTask, completeTask
)
from recolectores.permissions import IsAdmin, IsRecolector, IsEmpleado

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializers = {
        'default': OrdenListSerializer,
        'update': OrdenUpdateSerializer,
        'create': OrdenCreateSerializer,
    }
    http_method_names = ['get', 'post', 'put', 'delete']  # Eliminar 'patch'

    def get_permissions(self):
        """
        Asigna permisos basados en la acción. Por ejemplo, solo los admins pueden crear, actualizar o eliminar.
        """
        if self.action in ['update', 'retrieve']:
            permission_classes = [IsEmpleado]
        elif self.action in ['create']:
            permission_classes = [IsRecolector]
        else:
            permission_classes = [IsAdmin]
        
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    @extend_schema(
        summary="Obtener todas las ordenes",
        description="Devuelve una lista de todas las ordenes en el sistema",
        tags=["Ordenes"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Crear una nueva orden",
        description="Crea una nueva orden en el sistema y la envía a Bonita para procesamiento",
        tags=["Ordenes"]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Guardar la orden en la base de datos
            orden = serializer.save()

            # Procesar la orden en Bonita
            try:
                self.procesar_bonita(orden)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                messages.error(request, f"Error en el proceso de Bonita: {str(e)}")
                return Response({"detail": "Error en el proceso de Bonita"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def procesar_bonita(self, orden):
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
            assignVariableByTaskAndCase(token, session_id, case_id, 'cantidad', int(orden.cantidad_inicial), 'java.lang.Integer')
            assignVariableByTaskAndCase(token, session_id, case_id, 'deposito', orden.deposito.name, 'java.lang.String')
            assignVariableByTaskAndCase(token, session_id, case_id, 'orden_id', orden.id, 'java.lang.Integer')

            # 7. Obtengo el userId del usuario por username
            user_id = getUserIdByUsername(token, session_id)

            # 8. Asigno la actividad al usuario
            assignUserToTask(token, session_id, task_id, user_id)

            # 9. Completo la actividad asi avanza el proceso
            completeTask(token, session_id, task_id)

        except Exception as e:
            raise Exception(f"Error en el proceso de Bonita: {str(e)}")

    @extend_schema(
        summary="Obtener una orden por ID",
        description="Devuelve los detalles de una orden especificada por su ID",
        tags=["Ordenes"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar una orden por ID",
        description="Actualiza una orden en el sistema por su ID",
        tags=["Ordenes"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar una orden por ID",
        description="Elimina una orden en el sistema por su ID",
        tags=["Ordenes"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)