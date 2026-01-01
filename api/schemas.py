# Defines Pydantic schemas for order input, update, and API responses.
# Used for request validation and consistent response serialization.
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class OrderItem(BaseModel):
    # Represents a single item within an order
    product_id: str
    name: str
    price: float
    quantity: int


class OrderCreate(BaseModel):
    # Payload used when creating a new order
    user_id: str
    items: List[OrderItem]
    total_price: float
    status: str


class OrderUpdate(BaseModel):
    # Partial update payload (only provided fields will be updated)
    status: Optional[str] = None


class OrderOut(BaseModel):
    # Output schema for API responses, mapping MongoDB _id to id
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    user_id: str
    items: List[OrderItem]
    total_price: float
    status: str
