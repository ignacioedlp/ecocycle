from rest_framework import viewsets
from recolectores.models import Material
from recolectores.api.serializers import MaterialSerializer
from drf_spectacular.utils import extend_schema
from recolectores.permissions import IsAdmin
from rest_framework.permissions import AllowAny

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.filter(hide=False)
    serializer_class = MaterialSerializer
    http_method_names = ['get', 'post', 'put', 'delete']  # Eliminar 'patch'

    def get_permissions(self):
        """
        Asigna permisos basados en la acción. Por ejemplo, solo los admins pueden crear, actualizar o eliminar.
        """
        if self.action in ['list']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdmin]

        return [permission() for permission in permission_classes]

    @extend_schema(
        summary="Obtener todos los materiales",
        description="Devuelve una lista de todos los materiales en el sistema",
        tags=["Materiales"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Crear un nuevo material",
        description="Crea un nuevo material en el sistema",
        tags=["Materiales"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Obtener un material por ID",
        description="Devuelve los detalles de un material especificado por su ID",
        tags=["Materiales"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar un material por ID",
        description="Actualiza un material en el sistema por su ID",
        tags=["Materiales"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar un material por ID",
        description="Elimina un material en el sistema por su ID",
        tags=["Materiales"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    