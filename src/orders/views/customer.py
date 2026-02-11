from rest_framework import viewsets
from orders.models import Customer
from orders.serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.prefetch_related("proposals").all()
    serializer_class = CustomerSerializer