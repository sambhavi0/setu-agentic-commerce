import json
from pathlib import Path

from app.schemas.product import Product, ProductFilters


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "products.json"
)


def load_products() -> list[Product]:
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Product(**product) for product in data]


def list_products(filters: ProductFilters) -> list[Product]:
    products = load_products()

    results = products

    if filters.category:
        category = filters.category.strip().lower()

        results = [
            product
            for product in results
            if product.category.lower() == category
        ]

    if filters.min_price is not None:
        results = [
            product
            for product in results
            if product.price >= filters.min_price
        ]

    if filters.max_price is not None:
        results = [
            product
            for product in results
            if product.price <= filters.max_price
        ]

    if filters.search:
        search_term = filters.search.strip().lower()

        results = [
            product
            for product in results
            if (
                search_term in product.name.lower()
                or search_term in product.description.lower()
                or search_term in product.category.lower()
            )
        ]

    if filters.in_stock_only:
        results = [
            product
            for product in results
            if product.stock > 0
        ]

    return results


def get_product(product_id: str) -> Product | None:
    products = load_products()

    for product in products:
        if product.id == product_id:
            return product

    return None