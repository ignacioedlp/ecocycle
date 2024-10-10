from django.contrib import admin
from .models import Material, DepositoComunal, Orden, UserMaterial, Reserva

# Registro del modelo Material
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hide')
    search_fields = ('name',)
    list_filter = ('hide',)

# Registro del modelo DepositoComunal
@admin.register(DepositoComunal)
class DepositoComunalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hide')
    search_fields = ('name',)
    list_filter = ('hide',)

# Registro del modelo Orden
@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    # Custom name for the model
    verbose_name = 'Ordenes'
    list_display = ('id', 'estado', 'recolector', 'empleado', 'material', 'deposito', 'cantidad_inicial', 'cantidad_final', 'created_at', 'updated_at')
    search_fields = ('estado', 'recolector__username', 'empleado__username', 'material__name', 'deposito__name')
    list_filter = ('estado', 'material', 'deposito', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

# Registro del modelo UserMaterial
@admin.register(UserMaterial)
class UserMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'material', 'created_at', 'updated_at')
    search_fields = ('user__username', 'material__name')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'material','cantidad', 'estado', 'created_at', 'updated_at')
    search_fields = ('user__username', 'material__name')
    list_filter = ('estado', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
