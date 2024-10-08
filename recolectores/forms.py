from django import forms
from django.core.validators import MinValueValidator
from .models import Material, DepositoComunal, Orden

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['material', 'cantidad_inicial', 'deposito']

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

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
