from recolectores.api.views.pagos_views import PagosViewSet
from recolectores.api.views.notificacion_views import NotificacionViewSet
from rest_framework.routers import DefaultRouter
from recolectores.api.views.order_views import OrdenViewSet
from recolectores.api.views.material_views import MaterialViewSet
from recolectores.api.views.deposito_views import DepositoComunalViewSet
from recolectores.api.views.reserva_views import ReservaViewSet, ReservaByMaterialView, CompleteReservaView, TakeReservaView
from recolectores.api.views.auth_views import CustomTokenObtainPairView, CustomTokenRefreshView, Register
from recolectores.api.views.fabricante_views import QueryFabricanteMaterialView, AssignFabricanteMaterialView
from django.urls import path

router = DefaultRouter()
router.register(r'ordenes', OrdenViewSet, basename='orden')
router.register(r'materiales', MaterialViewSet, basename='material')
router.register(r'depositos-comunales', DepositoComunalViewSet, basename='deposito-comunal')
router.register(r'reservas', ReservaViewSet, basename='reserva')
router.register(r'pagos', PagosViewSet, basename='pagos')
router.register(r'notificacion-discrepancia',NotificacionViewSet, basename='notificacion-discrepancia')

urlpatterns = router.urls        

# Añade las rutas de JWT manualmente
urlpatterns += [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', Register, name='register'),
    path('material/<int:material_id>/reservas/', ReservaByMaterialView.as_view(), name='reservas-by-material'),
    path('material/<int:material_id>/query-fabricante/', QueryFabricanteMaterialView.as_view(), name='fabricantes-by-material'),
    path('material/<int:material_id>/assign-fabricante/', AssignFabricanteMaterialView.as_view(), name='assign-fabricante'),
    path('reserva/<int:reserva_id>/take-reserva/', TakeReservaView.as_view(), name='take-reserva'),
    path('reserva/<int:reserva_id>/complete-reserva/', CompleteReservaView.as_view(), name='complete-reserva'),
]
