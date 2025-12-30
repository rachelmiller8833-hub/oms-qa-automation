from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class OrderItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int


class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]
    total_price: float
    status: str


class OrderUpdate(BaseModel):
    status: Optional[str] = None


class OrderOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    user_id: str
    items: List[OrderItem]
    total_price: float
    status: str
