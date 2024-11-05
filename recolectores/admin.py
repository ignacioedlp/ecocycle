from django.contrib import admin
from .models import UserMaterial, Reserva

@admin.register(UserMaterial)
class UserMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor__username', 'material_id', 'created_at', 'updated_at')
    search_fields = ('proveedor__username', 'material_id')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'solicitante__username', 'material_id', 'cantidad', 'estado', 'deposito_encargado_id', 'created_at', 'updated_at')
    search_fields = ('solicitante__username', 'material_id')
    list_filter = ('estado', 'created_at', 'updated_at')