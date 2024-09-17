from rest_framework import serializers
from recolectores.models import Orden

class OrdenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = ['dni', 'material', 'cantidad']

class OrdenListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = ['id', 'dni', 'material', 'cantidad', 'estado', 'created_at', 'updated_at']

class OrdenUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = ['estado', 'dni', 'material', 'cantidad']