import json
from pathlib import Path
from app.schemas.mandate import Mandate

_MANDATE_PATH = Path(__file__).resolve().parent.parent / "data" / "mandate.json"

def get_active_mandate() -> Mandate:
    with open(_MANDATE_PATH, "r") as f:
        data = json.load(f)
    return Mandate(**data)