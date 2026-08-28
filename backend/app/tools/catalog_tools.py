from app.schemas.product import ProductFilters
from app.services.catalog_service import (
    list_products,
    get_product,
)
from app.services.purchase_service import initiate_purchase


def list_products_tool(
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
        "products": [
            product.model_dump()
            for product in products
        ],
        "count": len(products),
    }


def get_product_tool(product_id: str):
    product = get_product(product_id)

    if product is None:
        return {
            "success": False,
            "error": "PRODUCT_NOT_FOUND",
            "product_id": product_id,
        }

    return {
        "success": True,
        "product": product.model_dump(),
    }


def initiate_purchase_tool(
    product_id: str,
    quantity: int,
):
    return initiate_purchase(
        product_id=product_id,
        quantity=quantity,
    )