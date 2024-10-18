from rest_framework import viewsets, status
from recolectores.models import Reserva, UserMaterial
from recolectores.api.serializers import ReservaCreateSerializer, ReservaListSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from recolectores.helpers.bonita_helpers import (
    authenticate, getProcessId, initProcess, getTaskByCase, 
    assignVariableByTaskAndCase, getUserIdByUsername, assignUserToTask, completeTask
)
from recolectores.permissions import IsAdmin, IsFabricante
    
class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializers = {
        'default': ReservaListSerializer,
        'create': ReservaCreateSerializer,
    }
    http_method_names = ['get', 'post', 'put', 'delete']  # Eliminar 'patch'

    def get_permissions(self):
        """
        Asigna permisos basados en la acción. Por ejemplo, solo los admins pueden crear, actualizar o eliminar.
        """
        if self.action in ['destroy', 'create']:
            permission_classes = [IsFabricante]
        else:
            permission_classes = [IsAdmin]
        
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    @extend_schema(
        summary="Obtener todas las reservas",
        description="Devuelve una lista de todas las reservas en el sistema",
        tags=["Reservas"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Crear una nueva reserva",
        description="Crea una nueva reserva en el sistema y la envía a Bonita para procesamiento",
        tags=["Reservas"]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Guardar la reserva en la base de datos
            reserva = serializer.save()

            # Tomamos el user que esta authenticado y lo asignamos al recolector
            reserva.user = request.user
            reserva.save()

            # Procesar la reserva en Bonita
            try:

                existe = UserMaterial.objects.filter(user_id = reserva.user.id, material_id = reserva.material.id).exists()

                if (not existe):
                    UserMaterial.objects.create(user = reserva.user, material = reserva.material)

                # self.procesar_bonita(reserva, existe)
                return Response({
                    "id": reserva.id,
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"detail": "Error en el proceso de Bonita"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def procesar_bonita(self, reserva, existe):
        try:
            # 1. Me autentico en Bonita
            token, session_id = authenticate()

            # 2. Obtengo el ID del proceso de la reserva
            process_id = getProcessId(token, session_id, 'Reserva')

            # 3. Instancio el proceso
            case_id = initProcess(token, session_id, process_id)

            # 4. Agrego a la reserva el caseId del proceso
            reserva.case_bonita_id = case_id
            reserva.save()

            # 5. Busco la actividad por caso
            task_id = getTaskByCase(token, session_id, case_id)

            # 6. Asigno las variables de la actividad
            assignVariableByTaskAndCase(token, session_id, case_id, 'user_id', reserva.user.id, 'java.lang.Integer')
            assignVariableByTaskAndCase(token, session_id, case_id, 'primera_vez', 1 if not existe else 0, 'java.lang.Integer')
            assignVariableByTaskAndCase(token, session_id, case_id, 'material_id', reserva.material.id, 'java.lang.Integer')
            assignVariableByTaskAndCase(token, session_id, case_id, 'cantidad', int(reserva.cantidad), 'java.lang.Integer')
            assignVariableByTaskAndCase(token, session_id, case_id, 'reserva_id', reserva.id, 'java.lang.Integer')

            # 7. Obtengo el userId del usuario por username
            user_id = getUserIdByUsername(token, session_id)

            # 8. Asigno la actividad al usuario
            assignUserToTask(token, session_id, task_id, user_id)

            # 9. Completo la actividad asi avanza el proceso
            completeTask(token, session_id, task_id)

        except Exception as e:
            raise Exception(f"Error en el proceso de Bonita: {str(e)}")

    @extend_schema(
        summary="Obtener un reserva por ID",
        description="Devuelve los detalles de un reserva especificado por su ID",
        tags=["Reservas"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar un reserva por ID",
        description="Actualiza un reserva en el sistema por su ID",
        tags=["Reservas"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Cancelar un reserva por ID",
        description="Cancelar una reserva en el sistema por su ID",
        tags=["Reservas"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)