from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field


router = APIRouter(prefix="/orders", tags=["orders"])
orders: dict[str, "Order"] = {}


class CreateOrderRequest(BaseModel):
    customer_id: str = Field(min_length=1, max_length=100)
    item: str = Field(min_length=1, max_length=200)


class Order(BaseModel):
    id: str
    customer_id: str
    item: str


@router.get("", response_model=list[Order])
def list_orders() -> list[Order]:
    return list(orders.values())


@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(request: CreateOrderRequest) -> Order:
    order = Order(id=str(uuid4()), customer_id=request.customer_id, item=request.item)
    orders[order.id] = order
    return order


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str) -> Order:
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order