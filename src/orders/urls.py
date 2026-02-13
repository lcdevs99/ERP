from rest_framework.routers import DefaultRouter
from orders.views import CustomerViewSet, ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = router.urls