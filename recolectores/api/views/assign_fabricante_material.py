from rest_framework.response import Response
from rest_framework.views import APIView
from recolectores.models import UserMaterial
from recolectores.api.serializers import ReservaListSerializer
from drf_spectacular.utils import extend_schema
from recolectores.permissions import IsFabricante

@extend_schema(
    summary="Asignar un material a el fabricante",
    description="Asignar un material a el fabricante",
    tags=["Fabricantes"]
)
class AssignFabricanteMaterialView(APIView):
    # Aplica el permission_classes a nivel de clase
    permission_classes = [IsFabricante]

    # No necesitas @api_view en un método dentro de una APIView
    def get(self, request, material_id):
        """
        Asigna un material a un fabricante
        """

        fabricante = request.user
        if fabricante is not None:
            # si el material ya esta asignado el fabricante con el id material_id no se asigna
            existe = UserMaterial.objects.filter(user_id = fabricante.id, material_id = material_id).exists()
            if not existe:
                UserMaterial.objects.create(user_id = fabricante.id, material_id = material_id)
            return Response({'success': 'Material asignado a fabricante'})
        else:
            return Response({'error': 'Debe enviar un fabricante'})
