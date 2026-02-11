from rest_framework.routers import DefaultRouter
from orders.views import CustomerViewSet, LoanProposalViewSet

router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"loan-proposals", LoanProposalViewSet, basename="loanproposal")

urlpatterns = router.urls