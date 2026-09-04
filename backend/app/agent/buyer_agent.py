import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.tools.catalog_tools import (
    list_products_tool,
    get_product_tool,
    initiate_purchase_tool,
)

load_dotenv()

SYSTEM_PROMPT = """You are Setu's shopping agent, acting on behalf of a buyer under a spending mandate.

When the user expresses clear intent to buy something:
1. Use list_products and/or get_product to find a matching item.
2. ALWAYS call initiate_purchase to attempt it, even if the price looks high or borderline to you.
3. Never decide on your own whether confirmation is needed — the mandate/policy engine decides that, not you.
4. Report back exactly what initiate_purchase returns: if status is 'approved', confirm the purchase; if 'needs_confirmation', 'blocked_over_limit', 'blocked_category', or 'blocked_expired', explain the exact reason returned by the system.

Do not skip calling initiate_purchase under any circumstances when the user wants to buy something."""


@tool
def list_products(category: str | None = None, min_price: float | None = None,
                   max_price: float | None = None, search: str | None = None,
                   in_stock_only: bool = False) -> dict:
    """Search the merchant's product catalog with optional filters."""
    return list_products_tool(
        category=category, min_price=min_price, max_price=max_price,
        search=search, in_stock_only=in_stock_only,
    )


@tool
def get_product(product_id: str) -> dict:
    """Get full details for one product by its id."""
    return get_product_tool(product_id)


@tool
def initiate_purchase(product_id: str, quantity: int = 1) -> dict:
    """Attempt to purchase a product. Checked against stock and a spending mandate before completing."""
    return initiate_purchase_tool(product_id=product_id, quantity=quantity)

model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv(" "),
)

agent = create_react_agent(
    model,
    tools=[list_products, get_product, initiate_purchase],
    prompt=SYSTEM_PROMPT,
)


def run_agent(user_message: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": user_message}]})
    return result["messages"][-1].content