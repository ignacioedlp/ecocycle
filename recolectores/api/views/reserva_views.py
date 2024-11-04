from rest_framework import viewsets, status
from recolectores.models import Reserva, UserMaterial
from recolectores.api.serializers import ReservaCreateSerializer, ReservaListSerializer, TakeReservaSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.views import APIView
from recolectores.models import Reserva
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticated

@extend_schema(
    summary="Obtener las reservas pendientes para un material",
    description="Obtener las reservas pendientes para un material",
    tags=["Reservas"],
    parameters=[
        OpenApiParameter(
            name="fecha_inicio",
            description="Fecha de inicio del rango (formato YYYY-MM-DD)",
            required=True,
            type=OpenApiTypes.DATE
        ),
        OpenApiParameter(
            name="fecha_fin",
            description="Fecha de fin del rango (formato YYYY-MM-DD)",
            required=True,
            type=OpenApiTypes.DATE
        ),
    ]
)
class ReservaByMaterialView(APIView):
    # Aplica el permission_classes a nivel de clase
    permission_classes = [IsAuthenticated]

    # No necesitas @api_view en un método dentro de una APIView
    def get(self, request, material_id):
        reservas = Reserva.objects.filter(material_id=material_id, estado=Reserva.PENDIENTE)

        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        if fecha_inicio or fecha_fin:
            if fecha_inicio:
                fecha_inicio = parse_date(fecha_inicio)
                if not fecha_inicio:
                    raise ValidationError({"fecha_inicio": "Formato de fecha inválido. Use YYYY-MM-DD."})
                reservas = reservas.filter(fecha_prevista__gte=fecha_inicio)

            if fecha_fin:
                fecha_fin = parse_date(fecha_fin)
                if not fecha_fin:
                    raise ValidationError({"fecha_fin": "Formato de fecha inválido. Use YYYY-MM-DD."})
                reservas = reservas.filter(fecha_prevista__lte=fecha_fin)

        serializer = ReservaListSerializer(reservas, many=True)
        return Response(serializer.data)


@extend_schema(
    summary="Toma una reserva concreata",
    description="Toma una reserva concreata",
    tags=["Reservas"]
)
class TakeReservaView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TakeReservaSerializer

    def post(self, request, reserva_id):
        """
        Toma una reserva para un deposito en especifico enviado por el body
        """

        deposito_encargado_id = request.data.get('deposito_encargado_id')
        reserva = Reserva.objects.get(id = reserva_id)

        if reserva is None or reserva.estado != 'Pendiente':
            return Response({'error': 'La reserva no existe o ya fue procesada'})

        if deposito_encargado_id is None:
            return Response({'error': 'Debe enviar un deposito id'})
        else:
            reserva.estado = Reserva.PROCESADO
            reserva.deposito_encargado_id = deposito_encargado_id
            reserva.save()
            return Response({'success': 'La reserva fue tomada con exito'})
    

@extend_schema(
    summary= "Se completa una reserva",
    description= "Se completa una reserva",
    tags=["Reservas"]
)
class CompleteReservaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, reserva_id):
        """
        Completar una reserva
        """

        reserva = Reserva.objects.get(id = reserva_id)

        if reserva is None or reserva.estado != 'Procesado':
            return Response({'error': 'La reserva no existe, no fue tomada o ya fue completada'})
    

        deposito = reserva.deposito_encargado_id

        if deposito is not None:
            reserva.fecha_entrega = timezone.now()
            reserva.estado = Reserva.COMPLETADO
            reserva.save()
            return Response({'success': 'Reserva completa con exito'})
        else:
            return Response({'error': 'El deposito no tiene stock suficiente para completar la reserva'})
    
class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializers = {
        'default': ReservaListSerializer,
        'create': ReservaCreateSerializer,
    }
    http_method_names = ['get', 'post', 'put', 'delete']  # Eliminar 'patch'

    def get_permissions(self):
        """
        Asigna permisos basados en la acción. Ahora solo permite el acceso a usuarios autenticados.
        """
        permission_classes = [IsAuthenticated]  # Cambiado para permitir solo usuarios autenticados
        
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    @extend_schema(
        summary="Obtener todas las reservas",
        description="Devuelve una lista de todas las reservas en el sistema",
        tags=["Reservas"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Crear una nueva reserva",
        description="Crea una nueva reserva en el sistema y la envía a Bonita para procesamiento",
        tags=["Reservas"]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Guardar la reserva en la base de datos
            reserva = serializer.save()

            try:

                existe = UserMaterial.objects.filter(proveedor_id = reserva.solicitante.id, material_id = reserva.material_id).exists()

                if (not existe):
                    UserMaterial.objects.create(proveedor = reserva.solicitante, material_id = reserva.material_id)

                # self.procesar_bonita(reserva, existe)
                return Response({
                    "id": reserva.id,
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"detail": "Error en el proceso de Bonita"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Obtener un reserva por ID",
        description="Devuelve los detalles de un reserva especificado por su ID",
        tags=["Reservas"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar un reserva por ID",
        description="Actualiza un reserva en el sistema por su ID",
        tags=["Reservas"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Cancelar un reserva por ID",
        description="Cancelar una reserva en el sistema por su ID",
        tags=["Reservas"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)