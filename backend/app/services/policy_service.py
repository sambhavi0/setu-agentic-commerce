from datetime import datetime, timezone
from app.schemas.mandate import Mandate
from app.schemas.product import Product  

def evaluate_purchase(mandate: Mandate, product: Product, quantity: int) -> dict:
    total = product.price * quantity

    if datetime.now(timezone.utc) > mandate.expires_at:
        return {"status": "blocked_expired", "reason": f"Mandate {mandate.mandate_id} expired at {mandate.expires_at}."}

    if product.category not in mandate.allowed_categories:
        return {"status": "blocked_category", "reason": f"'{product.category}' is not in the allowed categories for this mandate."}

    if total > mandate.max_transaction:
        return {"status": "blocked_over_limit", "reason": f"₹{total} exceeds max transaction limit of ₹{mandate.max_transaction}."}

    if total > mandate.require_confirmation_above:
        return {"status": "needs_confirmation", "reason": f"₹{total} exceeds the ₹{mandate.require_confirmation_above} auto-approval threshold — human confirmation required."}

    return {"status": "approved", "reason": f"₹{total} within mandate limits and allowed category '{product.category}'."}