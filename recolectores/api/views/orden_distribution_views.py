from rest_framework import viewsets, status
from recolectores.models import OrdenDistribucion, Reserva, StockDeposito
from recolectores.api.serializers import OrdenDistribucionSerializer, OrdenDistribucionCreateSerializer
from drf_spectacular.utils import extend_schema
from recolectores.permissions import IsAdmin, IsEmpleado
from rest_framework.response import Response

class OrdenDistribucionViewSet(viewsets.ModelViewSet):
    queryset = OrdenDistribucion.objects
    serializers = {
        'default': OrdenDistribucionSerializer,
        'create': OrdenDistribucionCreateSerializer,
    }
    http_method_names = ['get', 'post', 'put', 'delete']  # Eliminar 'patch'

    def get_permissions(self):
        """
        Asigna permisos basados en la acción. Por ejemplo, solo los admins pueden crear, actualizar o eliminar.
        """
        permission_classes = [IsAdmin]
        if self.action in ['create']:
            permission_classes = [IsEmpleado]
        else:
            permission_classes = [IsAdmin]


        return [permission() for permission in permission_classes]
    
    
    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    @extend_schema(
        summary="Obtener todas las ordenes de distribucion",
        description="Devuelve una lista de todas las ordenes de distribucion en el sistema",
        tags=["Ordenes de distribucion"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Crear una nueva orden de distribucion",
        description="Crea una nueva orden de distribucion en el sistema",
        tags=["Ordenes de distribucion"]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            # Obtenemos el total de stock para el material y deposito especificados
            stock = StockDeposito.objects.filter(
                material=serializer.validated_data['material'],
                deposito=serializer.validated_data['deposito']
            ).first()

            # Si no hay stock, retornamos un error
            if not stock:
                return Response(
                    {"detail": "No hay stock disponible para el material y deposito especificados."},
                    status=status.HTTP_200_OK
                )
            
            #  reviso cuantas reservas tengo pendientes para este material y con la cantidad menor o igual al stock
            reservas = Reserva.objects.filter(
                material=serializer.validated_data['material'],
                estado='Pendiente'
            ).order_by('created_at')

            # Me quedo con los ids de las ordenes que puedo satisfacer con el stock
            reservas_ids = []

            for reserva in reservas:
                if stock.cantidad >= reserva.cantidad:
                    stock.cantidad -= reserva.cantidad
                    reservas_ids.append(reserva.id)
                    reserva.estado = Reserva.PROCESADO
                    reserva.save()
                    stock.save()

            # Creo una nueva orden de distribucion por cada reserva satisfecha
            for reserva_id in reservas_ids:
                OrdenDistribucion.objects.create(
                    reserva_id=reserva_id,
                    deposito=serializer.validated_data['deposito'],
                )

            return Response({
                "detail": "Ordenes de distribucion creadas exitosamente."
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Obtener una orden de distribucion por ID",
        description="Devuelve los detalles de una orden de distribucion especifica por su ID",
        tags=["Ordenes de distribucion"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar una orden de distribucion por ID",
        description="Actualiza una orden de distribucion en el sistema por su ID",
        tags=["Ordenes de distribucion"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar una orden de distribucion por ID",
        description="Elimina una orden de distribucion en el sistema por su ID",
        tags=["Ordenes de distribucion"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    