from datetime import datetime, timezone

_audit_log: list[dict] = []

def log_audit_event(event: dict) -> None:
    event["timestamp"] = datetime.now(timezone.utc).isoformat()
    _audit_log.append(event)
    print(f"[AUDIT] {event}")  # so you can see it live while testing

def get_audit_log() -> list[dict]:
    return _audit_log