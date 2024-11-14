from rest_framework import serializers
from recolectores.models import Reserva
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']


class ReservaCreateSerializer(serializers.ModelSerializer):
    solicitante_username = serializers.CharField()  # Cambiado a campo de entrada

    class Meta:
        model = Reserva
        fields = ['material_id', 'cantidad', 'fecha_prevista', 'solicitante_username', 'case_bonita_id']  # Modificado

    def validate_cantidad(self, value):
        if value < 1:
            raise serializers.ValidationError("La cantidad debe ser al menos 1.")
        return value

    def create(self, validated_data):
        solicitante_username = validated_data.pop('solicitante_username')  # Obtener el username del validated_data
        try:
            user = User.objects.get(username=solicitante_username)  # Buscar el usuario por username
        except User.DoesNotExist:
            raise serializers.ValidationError("El usuario no existe.")  # Manejo de error si el usuario no se encuentra

        reserva = Reserva.objects.create(solicitante=user, **validated_data)  # Asignar el usuario a la reserva
        return reserva

class ReservaListSerializer(serializers.ModelSerializer):
    solicitante_username = serializers.CharField(source='solicitante.username', read_only=True)

    class Meta:
        model = Reserva
        fields = ['id', 'material_id', 'cantidad', 'estado', 'case_bonita_id', 'created_at', 'updated_at', 'fecha_prevista', 'deposito_encargado_id', 'solicitante_username']

class TakeReservaSerializer(serializers.Serializer):
    deposito_encargado_id = serializers.IntegerField()
    class Meta:
        fields = ['deposito_encargado_id']