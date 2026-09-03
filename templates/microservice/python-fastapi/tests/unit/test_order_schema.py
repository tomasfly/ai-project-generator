import pytest
from pydantic import ValidationError

from app.api.orders import CreateOrderRequest


def test_create_order_requires_customer_id() -> None:
    with pytest.raises(ValidationError):
        CreateOrderRequest(customer_id="", item="book")