from rest_framework.response import Response
from rest_framework import viewsets, status
from recolectores.models import  NotificacionDiscrepancia
from recolectores.api.serializers import  NotificacionDiscrepanciaSerializer, NotificacionDiscrepanciaCreateSerializer
from drf_spectacular.utils import extend_schema
from recolectores.permissions import IsAdmin, IsEmpleado, IsRecolector

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = NotificacionDiscrepancia.objects.all()
    serializer_class = NotificacionDiscrepanciaSerializer
    serializers = {
        'default': NotificacionDiscrepanciaSerializer,
        'create': NotificacionDiscrepanciaCreateSerializer,
    }
    http_method_names = ['get', 'post', 'put', 'delete'] 

    def get_permissions(self):
        """
        Asigna permisos basados en la acción. Por ejemplo, solo los admins pueden crear, actualizar o eliminar.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsRecolector]
        elif self.action in ['create']:
            permission_classes = [IsEmpleado]
        else:
            permission_classes = [IsAdmin]

        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    @extend_schema(
        summary="Obtener todas las notificaciones",
        description="Devuelve una lista de todas las notificaciones en el sistema",
        tags=["Notificaciones de Discrepancias"]
    )
    def list(self, request, *args, **kwargs):
        user = request.user
        notificaciones_discrepancias = NotificacionDiscrepancia.objects.filter(orden__recolector=user)
        serializer = self.get_serializer(notificaciones_discrepancias, many=True)
        return  Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Crear una nueva notificación",
        description="Crea una nueva notificación en el sistema",
        tags=["Notificaciones de Discrepancias"]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({
            "detail": "Notificacion de discrepancia creadas exitosamente."
        }, status=status.HTTP_201_CREATED)


    @extend_schema(
        summary="Obtener una notificación de discrepancia por ID",
        description="Devuelve los detalles de una notificación de discrepancia especificado por su ID",
        tags=["Notificaciones de Discrepancias"]
    )
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        notificacion = NotificacionDiscrepancia.objects.get(id=kwargs['pk'], orden__user=user)
        serializer = NotificacionDiscrepanciaSerializer(notificacion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Actualizar una notificación de discrepancia por ID",
        description="Actualiza una notificación de discrepancia en el sistema por su ID",
        tags=["Notificaciones de Discrepancias"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar una notificación de discrepancia por ID",
        description="Elimina una notificación de discrepancia en el sistema por su ID",
        tags=["Notificaciones de Discrepancias"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
