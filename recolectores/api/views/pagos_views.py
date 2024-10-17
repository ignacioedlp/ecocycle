from rest_framework.response import Response
from rest_framework import viewsets, status
from recolectores.models import Pago
from recolectores.api.serializers import PagoSerializer
from drf_spectacular.utils import extend_schema
from recolectores.permissions import IsAdmin, IsEmpleado, IsRecolector

class PagosViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
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

    @extend_schema(
        summary="Obtener todos los pagos",
        description="Devuelve una lista de todos los pagos en el sistema",
        tags=["Pagos"]
    )
    def list(self, request, *args, **kwargs):
        user = request.user
        pagos = Pago.objects.filter(user=user)
        serializer = PagoSerializer(pagos, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Crear un nuevo pago",
        description="Crea un nuevo pago en el sistema",
        tags=["Pagos"]
    )
    def create(self, request, *args, **kwargs):
        pago_serializer = PagoSerializer(data=request.data)
        pago_serializer.is_valid(raise_exception=True)
        orden = pago_serializer.validated_data['orden']
        monto = orden.cantidad_final * orden.material.precio
        pago = Pago.objects.create(orden=orden, monto=monto)
        pago.save()
        return Response(PagoSerializer(pago).data)


    @extend_schema(
        summary="Obtener un pago por ID",
        description="Devuelve los detalles de un pago especificado por su ID",
        tags=["Pagos"]
    )
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        pago = Pago.objects.get(id=kwargs['pk'], user=user)
        serializer = PagoSerializer(pago)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Actualizar un pago por ID",
        description="Actualiza un pago en el sistema por su ID",
        tags=["Pagos"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar un pago por ID",
        description="Elimina un pago en el sistema por su ID",
        tags=["Pagos"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
