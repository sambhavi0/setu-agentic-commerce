import os
import uuid
import time

USE_MOCK = os.getenv("USE_MOCK_RAZORPAY", "true").lower() == "true"

if not USE_MOCK:
    import razorpay
    client = razorpay.Client(
        auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET"))
    )


def create_order(amount_rupees: float, receipt: str) -> dict:
    """
    Mirrors Razorpay's real Orders API response shape:
    https://razorpay.com/docs/api/orders/
    """
    if USE_MOCK:
        return {
            "id": f"order_MOCK{uuid.uuid4().hex[:14]}",
            "entity": "order",
            "amount": int(amount_rupees * 100),   # Razorpay uses paise
            "currency": "INR",
            "receipt": receipt,
            "status": "created",
            "created_at": int(time.time()),
        }
    return client.order.create({
        "amount": int(amount_rupees * 100),
        "currency": "INR",
        "receipt": receipt,
    })


def create_payment_link(order_id: str, amount_rupees: float, description: str) -> dict:
    """
    Mirrors Razorpay's real Payment Links API response shape:
    https://razorpay.com/docs/api/payments/payment-links/
    """
    if USE_MOCK:
        link_id = f"plink_MOCK{uuid.uuid4().hex[:14]}"
        return {
            "id": link_id,
            "entity": "payment_link",
            "amount": int(amount_rupees * 100),
            "currency": "INR",
            "description": description,
            "short_url": f"https://mock.razorpay.local/pay/{link_id}",
            "status": "created",
            "reference_id": order_id,
        }
    return client.payment_link.create({
        "amount": int(amount_rupees * 100),
        "currency": "INR",
        "description": description,
        "reference_id": order_id,
    })