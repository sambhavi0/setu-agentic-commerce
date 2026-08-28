from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas.product import ProductFilters
from app.services.catalog_service import (
    list_products,
    get_product,
)
from app.services.purchase_service import initiate_purchase


router = APIRouter(
    prefix="/agent/tools",
    tags=["Agent Tools"],
)


@router.get("/products")
def agent_list_products(
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    in_stock_only: bool = False,
):
    filters = ProductFilters(
        category=category,
        min_price=min_price,
        max_price=max_price,
        search=search,
        in_stock_only=in_stock_only,
    )

    products = list_products(filters)

    return {
        "products": products,
        "count": len(products),
    }


@router.get("/products/{product_id}")
def agent_get_product(product_id: str):
    product = get_product(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product '{product_id}' not found",
        )

    return product


class PurchaseRequest(BaseModel):
    id: str
    quantity: int


@router.post("/initiate_purchase")
def agent_initiate_purchase(request: PurchaseRequest):
    return initiate_purchase(
        product_id=request.id,
        quantity=request.quantity,
    )