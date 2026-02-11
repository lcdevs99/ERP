from rest_framework import serializers
from orders.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "email", "cpf", "birth_date"]