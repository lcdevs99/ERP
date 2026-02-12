from rest_framework import serializers
from orders.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "cpf_cnpj", "email", "phone", "address", "status"]