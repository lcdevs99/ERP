import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from orders.models import Product


@pytest.mark.django_db
def test_create_product_success():
    client = APIClient()

    payload = {
        "sku": "SKU123",
        "name": "Produto Teste",
        "description": "Descrição teste",
        "price": "10.50",
        "stock": 20,
        "status": "ACTIVE",
    }

    response = client.post(reverse("product-list"), payload, format="json")

    assert response.status_code == 201
    assert Product.objects.count() == 1
    product = Product.objects.first()
    assert product.sku == "SKU123"
    assert product.stock == 20


@pytest.mark.django_db
def test_list_products():
    Product.objects.create(
        sku="SKU1", name="Produto 1", price=10, stock=5, status="ACTIVE"
    )
    Product.objects.create(
        sku="SKU2", name="Produto 2", price=20, stock=10, status="ACTIVE"
    )

    client = APIClient()
    response = client.get(reverse("product-list"))

    assert response.status_code == 200
    # Ajuste para paginação
    assert response.data["count"] == 2
    assert len(response.data["results"]) == 2
    assert response.data["results"][0]["sku"] in ["SKU1", "SKU2"]
    assert response.data["results"][1]["sku"] in ["SKU1", "SKU2"]


@pytest.mark.django_db
def test_update_product_stock_success():
    product = Product.objects.create(
        sku="SKU-STOCK",
        name="Produto Estoque",
        price=15,
        stock=10,
        status="ACTIVE",
    )

    client = APIClient()
    url = reverse("product-update-stock", args=[product.id])

    response = client.patch(url, {"stock": 30}, format="json")

    assert response.status_code == 200

    product.refresh_from_db()
    assert product.stock == 30


@pytest.mark.django_db
def test_update_product_stock_without_value():
    product = Product.objects.create(
        sku="SKU-ERR",
        name="Produto Erro",
        price=10,
        stock=5,
        status="ACTIVE",
    )

    client = APIClient()
    url = reverse("product-update-stock", args=[product.id])

    response = client.patch(url, {}, format="json")

    assert response.status_code == 400
    assert "error" in response.data