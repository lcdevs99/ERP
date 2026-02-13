from rest_framework import viewsets
from rest_framework import viewsets
from orders.models import Customer
from orders.serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()

    filterset_fields = ["status", "cpf_cnpj", "email"]
    ordering_fields = ["name", "email", "cpf_cnpj"]