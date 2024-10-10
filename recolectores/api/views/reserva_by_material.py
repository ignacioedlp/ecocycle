from rest_framework.response import Response
from rest_framework.views import APIView
from recolectores.models import Reserva
from recolectores.api.serializers import ReservaListSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny

@extend_schema(
    summary="Obtener las reservas pendientes para un material",
    description="Obtener las reservas pendientes para un material",
    tags=["Reservas"]
)
class ReservaByMaterialView(APIView):
    # Aplica el permission_classes a nivel de clase
    permission_classes = [AllowAny]

    # No necesitas @api_view en un método dentro de una APIView
    def get(self, request, material_id):
        reservas = Reserva.objects.filter(material__id=material_id, estado=Reserva.PENDIENTE)
        serializer = ReservaListSerializer(reservas, many=True)
        return Response(serializer.data)
