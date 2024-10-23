from rest_framework.response import Response
from rest_framework.views import APIView
from recolectores.models import Reserva, DepositoComunal, StockDeposito, OrdenDistribucion
from drf_spectacular.utils import extend_schema
from recolectores.permissions import IsEmpleado
from recolectores.api.serializers import CreateOrdenDistribucionReservaSerializer

@extend_schema(
    summary="Se crea una orden de distribucion para una reserva concreata",
    description="Se crea una orden de distribucion para una reserva concreata",
    tags=["Ordenes de distribucion"]
)
class CreateOrdenDistribucionReservaView(APIView):
    permission_classes = [IsEmpleado]
    serializer_class = CreateOrdenDistribucionReservaSerializer

    def post(self, request, reserva_id):
        """
        Crear una orden de distribucion de una reserva para un deposito en especifico enviado por el body
        """

        deposito_id = request.data.get('deposito_id')
        reserva = Reserva.objects.get(id = reserva_id)

        if reserva is None or reserva.estado != 'Pendiente':
            return Response({'error': 'La reserva no existe o ya fue procesada'})

        if deposito_id is None:
            return Response({'error': 'Debe enviar un deposito id'})
        else:
            deposito = DepositoComunal.objects.get(id = deposito_id)
            stock = StockDeposito.objects.filter(deposito = deposito, material = reserva.material).first()

            if deposito is not None and stock is not None and stock.cantidad >= reserva.cantidad:
                OrdenDistribucion.objects.create(reserva_id = reserva_id, deposito_id = deposito_id)
                stock.cantidad -= reserva.cantidad
                return Response({'success': 'Orden de distribucion creada'})
            else:
                return Response({'error': 'El deposito no tiene stock suficiente para la reserva'})
    

            