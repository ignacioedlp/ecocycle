from rest_framework.routers import DefaultRouter
from .views import OrdenViewSet, MaterialViewSet, DepositoComunalViewSet

router = DefaultRouter()
router.register(r'ordenes', OrdenViewSet, basename='orden')
router.register(r'materiales', MaterialViewSet, basename='material')
router.register(r'depositos-comunales', DepositoComunalViewSet, basename='deposito-comunal')

urlpatterns = router.urls
