from app.tools.catalog_tools import (
    list_products_tool,
    get_product_tool,
    initiate_purchase_tool,
)


print("\n--- LIST PRODUCTS ---")

result = list_products_tool(
    category="sneakers",
    max_price=3000,
    in_stock_only=True,
)

print(result)


print("\n--- GET PRODUCT ---")

result = get_product_tool("shoes-002")

print(result)


print("\n--- PURCHASE ---")

result = initiate_purchase_tool(
    product_id="shoes-001",
    quantity=1,
)

print(result)