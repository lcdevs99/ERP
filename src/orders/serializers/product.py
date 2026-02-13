from rest_framework import serializers
from orders.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "sku", "name", "description", "price", "stock", "status"]