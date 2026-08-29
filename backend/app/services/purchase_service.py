import uuid

from app.services.catalog_service import get_product
from app.services.policy_service import evaluate_purchase
from app.services.mandate_service import get_active_mandate
from app.services.audit_service import log_audit_event


def initiate_purchase(product_id: str, quantity: int):
    product = get_product(product_id)

    if product is None:
        return {
            "success": False,
            "error": "PRODUCT_NOT_FOUND",
            "message": f"Product '{product_id}' not found.",
        }

    if quantity <= 0:
        return {
            "success": False,
            "error": "INVALID_QUANTITY",
            "message": "Quantity must be greater than zero.",
        }

    if product.stock < quantity:
        return {
            "success": False,
            "error": "INSUFFICIENT_STOCK",
            "message": (
                f"Only {product.stock} units of "
                f"'{product.name}' are available."
            ),
        }

    mandate = get_active_mandate()
    decision = evaluate_purchase(mandate, product, quantity)

    log_audit_event({
        "action": "initiate_purchase",
        "product_id": product.id,
        "quantity": quantity,
        "decision": decision["status"],
        "reason": decision["reason"],
    })

    if decision["status"] != "approved":
        return {
            "success": False,
            "status": decision["status"],
            "reason": decision["reason"],
        }

    transaction_id = f"TX-{uuid.uuid4().hex[:8].upper()}"
    total_amount = product.price * quantity

    return {
        "success": True,
        "mode": "MOCK",
        "status": decision["status"],
        "reason": decision["reason"],
        "transaction_id": transaction_id,
        "product": {
            "id": product.id,
            "name": product.name,
        },
        "quantity": quantity,
        "unit_price": product.price,
        "total_amount": total_amount,
        "currency": product.currency,
        "payment_status": "PENDING_PAYMENT",
        "message": "Mock purchase initiated successfully.",
    }