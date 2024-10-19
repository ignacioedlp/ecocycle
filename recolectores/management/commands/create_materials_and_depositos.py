# custom command to create materials and depositos

import random
from django.core.management.base import BaseCommand
from recolectores.models import Material, DepositoComunal


class Command(BaseCommand):
    help = 'Create materials and depositos'

    def handle(self, *args, **options):
        materials = [
            'Plástico',
            'Vidrio',
            'Cartón',
            'Papel',
            'Metal',
        ]

        for material in materials:
            Material.objects.get_or_create(name=material)
            self.stdout.write(self.style.SUCCESS(f'Material {material} created'))

        depositos = [
            'La Plata, 1 y 60',
            'La Plata, 7 y 50',
            'La Plata, 13 y 32',
            'Los Hornos, 60 y 137',
            'Olmos, 44 y 197',
        ]

        for deposito in depositos:
            DepositoComunal.objects.get_or_create(name=deposito)
            self.stdout.write(self.style.SUCCESS(f'Deposito {deposito} created'))