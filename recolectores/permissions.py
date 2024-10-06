from rest_framework import permissions

class IsInGroup(permissions.BasePermission):
    """
    Permiso que verifica si el usuario pertenece a un grupo específico.
    """
    group_name = None

    def has_permission(self, request, view):
        # Verifica si el usuario está autenticado y pertenece al grupo especificado
        return request.user.is_authenticated and request.user.groups.filter(name=self.group_name).exists()

class IsAdmin(IsInGroup):
    group_name = 'Admin'

class IsRecolector(IsInGroup):
    group_name = 'Recolector'

class IsFabricante(IsInGroup):
    group_name = 'Fabricante'

class IsEmpleado(IsInGroup):
    group_name = 'Empleado'
