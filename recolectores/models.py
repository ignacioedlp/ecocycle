from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
class UserMaterial(models.Model):
    class Meta:
        db_table = 'fabricantes_materiales'

    proveedor = models.ForeignKey(User, on_delete=models.CASCADE)
    material_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Reserva(models.Model):
    class Meta:
        db_table = "reservas"

    PENDIENTE = 'Pendiente'
    PROCESADO = 'Procesado'
    CANCELADO = 'Cancelado'
    COMPLETADO = 'Completado'

    STATUS_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (PROCESADO, 'Procesado'),
        (CANCELADO, 'Cancelado'),
        (COMPLETADO, 'Completado')
    ]

    estado = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDIENTE,
    )

    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    material_id = models.IntegerField(blank=True, null=True)
    deposito_encargado_id = models.IntegerField(blank=True, null=True)
    fecha_prevista = models.DateField(blank=True, null=True)
    fecha_entrega = models.DateField(blank=True, null=True)
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    case_bonita_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
