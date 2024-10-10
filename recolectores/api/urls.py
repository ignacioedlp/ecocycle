from rest_framework.routers import DefaultRouter
from recolectores.api.views.order_views import OrdenViewSet
from recolectores.api.views.material_views import MaterialViewSet
from recolectores.api.views.deposito_views import DepositoComunalViewSet
from recolectores.api.views.reserva_views import ReservaViewSet
from recolectores.api.views.auth_views import CustomTokenObtainPairView, CustomTokenRefreshView, Register
from django.urls import path

router = DefaultRouter()
router.register(r'ordenes', OrdenViewSet, basename='orden')
router.register(r'materiales', MaterialViewSet, basename='material')
router.register(r'depositos-comunales', DepositoComunalViewSet, basename='deposito-comunal')
router.register(r'reservas', ReservaViewSet, basename='reserva')

urlpatterns = router.urls

# Añade las rutas de JWT manualmente
urlpatterns += [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', Register, name='register'),
]
