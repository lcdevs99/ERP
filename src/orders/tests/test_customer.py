import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from orders.models import Customer


@pytest.mark.django_db
def test_create_customer_success():
    client = APIClient()

    payload = {
        "name": "Cliente Teste",
        "cpf_cnpj": "12345678901",
        "email": "cliente@teste.com",
        "phone": "21999999999",
        "address": "Rua Teste, 123",
        "status": "ACTIVE",
    }

    response = client.post(reverse("customer-list"), payload, format="json")

    assert response.status_code == 201
    assert Customer.objects.count() == 1

    customer = Customer.objects.first()
    assert customer.name == "Cliente Teste"
    assert customer.status == "ACTIVE"


@pytest.mark.django_db
def test_list_customers():
    Customer.objects.create(
        name="Cliente 1",
        cpf_cnpj="11111111111",
        email="c1@teste.com",
        status="ACTIVE",
    )
    Customer.objects.create(
        name="Cliente 2",
        cpf_cnpj="22222222222",
        email="c2@teste.com",
        status="INACTIVE",
    )

    client = APIClient()
    response = client.get(reverse("customer-list"))

    assert response.status_code == 200
    # Ajuste para paginação
    assert response.data["count"] == 2
    assert len(response.data["results"]) == 2
    assert response.data["results"][0]["name"] in ["Cliente 1", "Cliente 2"]
    assert response.data["results"][1]["name"] in ["Cliente 1", "Cliente 2"]


@pytest.mark.django_db
def test_get_customer_by_id():
    customer = Customer.objects.create(
        name="Cliente Detalhe",
        cpf_cnpj="33333333333",
        email="detalhe@teste.com",
        status="ACTIVE",
    )

    client = APIClient()
    response = client.get(reverse("customer-detail", args=[customer.id]))

    assert response.status_code == 200
    assert response.data["id"] == customer.id


@pytest.mark.django_db
def test_customer_unique_email_constraint():
    Customer.objects.create(
        name="Cliente 1",
        cpf_cnpj="44444444444",
        email="unique@teste.com",
        status="ACTIVE",
    )

    client = APIClient()
    payload = {
        "name": "Cliente 2",
        "cpf_cnpj": "55555555555",
        "email": "unique@teste.com",
        "status": "ACTIVE",
    }

    response = client.post(reverse("customer-list"), payload, format="json")

    assert response.status_code == 400
