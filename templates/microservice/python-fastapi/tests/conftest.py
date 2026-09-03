import pytest

from app.api.orders import orders


@pytest.fixture(autouse=True)
def clear_orders() -> None:
    orders.clear()