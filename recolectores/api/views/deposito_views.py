from rest_framework import viewsets
from recolectores.models import DepositoComunal
from recolectores.api.serializers import DepositoComunalSerializer
from drf_spectacular.utils import extend_schema
from recolectores.permissions import IsAdmin

class DepositoComunalViewSet(viewsets.ModelViewSet):
    queryset = DepositoComunal.objects.filter(hide=False)
    serializer_class = DepositoComunalSerializer
    http_method_names = ['get', 'post', 'put', 'delete']  # Eliminar 'patch'

    def get_permissions(self):
        """
        Asigna permisos basados en la acción. Por ejemplo, solo los admins pueden crear, actualizar o eliminar.
        """
        permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    @extend_schema(
        summary="Obtener todos los depositos comunales",
        description="Devuelve una lista de todos los depositos comunales en el sistema",
        tags=["Depósitos Comunales"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Crear un nuevo depósito comunal",
        description="Crea un nuevo depósito comunal en el sistema",
        tags=["Depósitos Comunales"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Obtener un depósito comunal por ID",
        description="Devuelve los detalles de un depósito comunal especificado por su ID",
        tags=["Depósitos Comunales"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar un depósito comunal por ID",
        description="Actualiza un depósito comunal en el sistema por su ID",
        tags=["Depósitos Comunales"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar un depósito comunal por ID",
        description="Elimina un depósito comunal en el sistema por su ID",
        tags=["Depósitos Comunales"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
