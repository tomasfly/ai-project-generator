from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_creates_lists_and_reads_an_order() -> None:
    created = client.post("/api/v1/orders", json={"customer_id": "customer-1", "item": "book"})

    assert created.status_code == 201
    order = created.json()
    assert order["customer_id"] == "customer-1"

    listed = client.get("/api/v1/orders")
    assert listed.status_code == 200
    assert listed.json() == [order]

    fetched = client.get(f"/api/v1/orders/{order['id']}")
    assert fetched.status_code == 200
    assert fetched.json() == order