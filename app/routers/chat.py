from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.router import route_query

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

@router.post("")
def chat(request: ChatRequest):
    result = route_query(request.message)
    return {
        "message": request.message,
        "response": result["answer"],
        "intent": result["intent"]
    }
