from django import forms
from django.core.validators import MinValueValidator


class OrderForm(forms.Form):
    dni = forms.CharField(label="DNI", max_length=8)
    material = forms.CharField(label="Material", max_length=100)
    cantidad = forms.DecimalField(label="Cantidad", max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)])