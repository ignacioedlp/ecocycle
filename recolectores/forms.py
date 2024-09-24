from django import forms
from django.core.validators import MinValueValidator
from .models import Material, DepositoComunal, Orden

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['dni', 'material', 'cantidad_inicial', 'deposito']

    material = forms.ModelChoiceField(
        queryset=Material.objects.filter(hide=False),
        label="Material"
    )

    deposito = forms.ModelChoiceField(
        queryset=DepositoComunal.objects.filter(hide=False),
        label="Depósito"
    )

    cantidad_inicial = forms.DecimalField(
        label="Cantidad",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )