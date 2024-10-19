from rest_framework.response import Response
from rest_framework.views import APIView
from recolectores.models import UserMaterial
from recolectores.api.serializers import ReservaListSerializer
from drf_spectacular.utils import extend_schema
from recolectores.permissions import IsFabricante

@extend_schema(
    summary="Consulta si un material esta asignado a el fabricante",
    description="Consulta si un material esta asignado a el fabricante",
    tags=["Fabricantes"]
)
class QueryFabricanteMaterialView(APIView):
    # Aplica el permission_classes a nivel de clase
    permission_classes = [IsFabricante]

    # No necesitas @api_view en un método dentro de una APIView
    def get(self, request, material_id):
        """
        Devuelve un si un material esta asociado a un fabricante 1 si es la primera vez 0 si ya esta asignado
        """

        fabricante = request.user
        if fabricante is not None:
            existe = UserMaterial.objects.filter(user_id = fabricante.id, material_id = material_id).exists()
            return Response({'primera_vez': 1 if not existe else 0})
        else:
            return Response({'error': 'Debe enviar un fabricante'})