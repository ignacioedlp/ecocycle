from rest_framework.response import Response
from rest_framework.views import APIView
from recolectores.models import UserMaterial
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

@extend_schema(
    summary="Asignar un material a el fabricante",
    description="Asignar un material a el fabricante",
    tags=["Fabricantes"],
    parameters=[
        OpenApiParameter(
            name="fabricante_username",
            description="Fabricante",
            required=True,
            type=OpenApiTypes.STR
        ),
    ]
)
class AssignFabricanteMaterialView(APIView):
    # Aplica el permission_classes a nivel de clase
    permission_classes = [IsAuthenticated]

    # No necesitas @api_view en un método dentro de una APIView
    def get(self, request, material_id):
        """
        Asigna un material a un fabricante
        """

        fabricante_username = request.query_params.get('fabricante_username')
        if fabricante_username is not None:
            # Obtener el objeto User usando el username
            fabricante = User.objects.filter(username=fabricante_username).first()
            if fabricante is None:
                return Response({'error': 'Fabricante no encontrado'}, status=404)

            existe = UserMaterial.objects.filter(proveedor_id = fabricante.id, material_id = material_id).exists()
            if not existe:
                UserMaterial.objects.create(proveedor_id = fabricante.id, material_id = material_id)
            return Response({'success': 'Material asignado a fabricante'})
        else:
            return Response({'error': 'Debe enviar un fabricante'})

@extend_schema(
    summary="Consulta si un material esta asignado a el fabricante",
    description="Consulta si un material esta asignado a el fabricante",
    tags=["Fabricantes"],
    parameters=[
        OpenApiParameter(
            name="fabricante_username",
            description="Fabricante",
            required=True,
            type=OpenApiTypes.STR
        ),
    ]
)
class QueryFabricanteMaterialView(APIView):
    # Aplica el permission_classes a nivel de clase
    permission_classes = [IsAuthenticated]

    # No necesitas @api_view en un método dentro de una APIView
    def get(self, request, material_id):
        """
        Devuelve un si un material esta asociado a un fabricante 1 si es la primera vez 0 si ya esta asignado
        """

        fabricante_username = request.query_params.get('fabricante_username')
        if fabricante_username is not None:
            # Obtener el objeto User usando el username
            fabricante = User.objects.filter(username=fabricante_username).first()
            if fabricante is None:
                return Response({'error': 'Fabricante no encontrado'}, status=404)

            existe = UserMaterial.objects.filter(proveedor_id = fabricante.id, material_id = material_id).exists()
            return Response({'primera_vez': 1 if not existe else 0})