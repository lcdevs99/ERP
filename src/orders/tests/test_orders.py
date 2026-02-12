import pytest
from concurrent.futures import ThreadPoolExecutor
from django.urls import reverse
from rest_framework.test import APIClient
from orders.models import Product, Order, Customer


@pytest.mark.django_db(transaction=True)
def test_concurrent_stock_reservation():
    client = APIClient()
    customer = Customer.objects.create(
        name="Cliente Concorrência",
        email="concorrencia@teste.com",
        status="ACTIVE"
    )
    product = Product.objects.create(
        sku="PRODX",
        name="Produto X",
        price=10,
        stock=10,
        status="ACTIVE"
    )

    def create_order(key):
        response = client.post(reverse("order-list"), {
            "customer_id": customer.id,
            "items": [{"product_id": product.id, "quantity": 8}],
            "idempotency_key": key
        }, format="json")
        print("Response:", response.status_code, response.data)
        return response

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(create_order, "concurrency-1"),
            executor.submit(create_order, "concurrency-2")
        ]
        results = [f.result() for f in futures]

    success = sum(1 for r in results if r.status_code in (200, 201))
    fail = sum(1 for r in results if r.status_code == 400)

    assert success == 1
    assert fail == 1
    assert Order.objects.count() == 1


@pytest.mark.django_db
def test_order_idempotency():
    client = APIClient()
    customer = Customer.objects.create(
        name="Cliente Idempotência",
        email="idempotencia@teste.com",
        status="ACTIVE"
    )
    product = Product.objects.create(
        sku="PRODY",
        name="Produto Y",
        price=20,
        stock=50,
        status="ACTIVE"
    )

    payload = {
        "customer_id": customer.id,
        "items": [{"product_id": product.id, "quantity": 2}],
        "idempotency_key": "same-key"
    }

    responses = [client.post(reverse("order-list"), payload, format="json") for _ in range(3)]
    for r in responses:
        print("Response:", r.status_code, r.data)

    assert all(r.status_code in (200, 201) for r in responses)
    assert Order.objects.count() == 1


@pytest.mark.django_db(transaction=True)
def test_atomicity_on_partial_failure():
    client = APIClient()
    customer = Customer.objects.create(
        name="Cliente Atomicidade",
        email="atomicidade@teste.com",
        status="ACTIVE"
    )
    p1 = Product.objects.create(sku="ITEM1", name="Item 1", price=10, stock=10, status="ACTIVE")
    p2 = Product.objects.create(sku="ITEM2", name="Item 2", price=15, stock=5, status="ACTIVE")
    p3 = Product.objects.create(sku="ITEM3", name="Item 3", price=20, stock=0, status="ACTIVE")  # sem estoque

    payload = {
        "customer_id": customer.id,
        "items": [
            {"product_id": p1.id, "quantity": 2},
            {"product_id": p2.id, "quantity": 1},
            {"product_id": p3.id, "quantity": 1}
        ],
        "idempotency_key": "atomic-failure"
    }

    response = client.post(reverse("order-list"), payload, format="json")
    print("Response:", response.status_code, response.data)

    assert response.status_code == 400

    p1.refresh_from_db()
    p2.refresh_from_db()
    assert p1.stock == 10
    assert p2.stock == 5