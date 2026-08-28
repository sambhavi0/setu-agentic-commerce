from typing import Optional

from pydantic import BaseModel, Field


class PurchaseAction(BaseModel):
    type: str
    method: str
    endpoint: str
    input: dict


class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float
    currency: str
    stock: int
    description: str
    purchase_action: PurchaseAction


class ProductFilters(BaseModel):
    category: Optional[str] = None
    min_price: Optional[float] = Field(default=None, ge=0)
    max_price: Optional[float] = Field(default=None, ge=0)
    search: Optional[str] = None
    in_stock_only: bool = False