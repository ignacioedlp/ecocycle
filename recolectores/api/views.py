from rest_framework import viewsets
from recolectores.models import Orden
from recolectores.api.serializers import OrdenCreateSerializer, OrdenListSerializer, OrdenUpdateSerializer
from drf_spectacular.utils import extend_schema

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializers = {
        'default': OrdenListSerializer,
        'update': OrdenUpdateSerializer,
        'create': OrdenCreateSerializer,
    }
    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])


    @extend_schema(
        summary="Obtener todas las ordenes",
        description="Devuelve una lista de todas las ordenes en el sistema",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Crear una nueva orden",
        description="Crea una nueva orden en el sistema",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Obtener una orden por ID",
        description="Devuelve los detalles de una orden especificada por su ID",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar una orden por ID",
        description="Actualiza una orden en el sistema por su ID",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar una orden por ID",
        description="Elimina una orden en el sistema por su ID",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
