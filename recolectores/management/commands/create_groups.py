from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Creates default user groups: Admin, Recolector, Fabricante, Empleado'

    def handle(self, *args, **options):
        groups = ['Admin', 'Recolector', 'Fabricante', 'Empleado']
        
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group {group_name} created successfully!'))
            else:
                self.stdout.write(self.style.WARNING(f'Group {group_name} already exists.'))
