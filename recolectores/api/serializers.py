from rest_framework import serializers
from recolectores.models import Orden, Material, DepositoComunal
from django.contrib.auth.models import User

class OrdenCreateSerializer(serializers.ModelSerializer):
    material = serializers.PrimaryKeyRelatedField(
        queryset=Material.objects.filter(hide=False)
    )
    deposito = serializers.PrimaryKeyRelatedField(
        queryset=DepositoComunal.objects.filter(hide=False)
    )

    class Meta:
        model = Orden
        fields = ['dni', 'material', 'cantidad_inicial', 'deposito']

    def validate_cantidad_inicial(self, value):
        if value < 1:
            raise serializers.ValidationError("La cantidad inicial debe ser al menos 1.")
        return value


class OrdenListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = ['id', 'dni', 'material', 'cantidad_inicial', 'estado', 'case_bonita_id', 'created_at', 'updated_at']


class OrdenUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = ['cantidad_final']

class DepositoComunalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositoComunal
        fields = ['id', 'name', 'hide']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'hide']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']