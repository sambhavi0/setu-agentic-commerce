from pydantic import BaseModel
from typing import List
from datetime import datetime

class Mandate(BaseModel):
    mandate_id: str
    currency: str = "INR"
    max_transaction: float
    daily_limit: float
    allowed_categories: List[str]
    require_confirmation_above: float
    expires_at: datetime