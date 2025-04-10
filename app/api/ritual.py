# /api/ritual.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from shared.global_objects import managers
from services.ritual_session_service import ritual_service

router = APIRouter()

# Request Models
class StartRitualRequest(BaseModel):
    type: str  # "morning" or "evening"

class RespondRitualRequest(BaseModel):
    ritual_id: str
    user_message: str

# Response Model
class RitualResponse(BaseModel):
    ritual_id: str
    bot_message: str

@router.post("/start", response_model=RitualResponse)
def start_ritual(request: StartRitualRequest):
    ritual_type = request.type.lower()

    if ritual_type == "morning":
        starter_context = managers["morning_manager"].build_context_payload()
        opening_line = starter_context.get("starter_script", "Good morning, let's begin.")  # fallback
    elif ritual_type == "evening":
        starter_context = managers["evening_manager"].build_context_payload()
        opening_line = starter_context.get("starter_script", "Good evening, let's begin.")  # fallback
    else:
        raise HTTPException(status_code=400, detail="Invalid ritual type.")

    # Start a new ritual session
    ritual_id = ritual_service.start_custom_ritual(ritual_type, opening_line)

    return RitualResponse(ritual_id=ritual_id, bot_message=opening_line)

@router.post("/respond", response_model=RitualResponse)
def respond_ritual(request: RespondRitualRequest):
    bot_message = ritual_service.handle_response(request.ritual_id, request.user_message)
    if not bot_message:
        raise HTTPException(status_code=404, detail="Ritual session not found or already completed.")

    return RitualResponse(ritual_id=request.ritual_id, bot_message=bot_message)
