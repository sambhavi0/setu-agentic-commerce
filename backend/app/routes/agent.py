from fastapi import APIRouter
from pydantic import BaseModel

from app.agent.buyer_agent import run_agent
from app.services.audit_service import get_audit_log

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def agent_chat(request: ChatRequest):
    reply = run_agent(request.message)
    return {"reply": reply}


@router.get("/audit")
def agent_audit():
    return {"log": get_audit_log()}