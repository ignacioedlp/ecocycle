from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Orden(models.Model):
    class Meta:
        db_table = 'ordenes'

    PENDIENTE = 'Pendiente'
    PROCESADO = 'Procesado'
    CANCELADO = 'Cancelado'

    STATUS_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (PROCESADO, 'Procesado'),
        (CANCELADO, 'Cancelado'),
    ]

    estado = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDIENTE,
    )

    dni = models.CharField(max_length=8)
    material = models.CharField(max_length=100)
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
