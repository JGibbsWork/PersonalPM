# /api/ritual.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from shared import global_objects
from services.ritual_session_service import ritual_service

router = APIRouter()

class StartRitualRequest(BaseModel):
    type: str  # "morning" or "evening"

class RespondRitualRequest(BaseModel):
    ritual_id: str
    user_message: str

class RitualResponse(BaseModel):
    ritual_id: str
    bot_message: str

@router.post("/start", response_model=RitualResponse)
def start_ritual(request: StartRitualRequest):
    ritual_type = request.type.lower()

    if not global_objects.managers:
        raise HTTPException(status_code=500, detail="Managers not initialized")

    # Build Ritual
    ritual_builder = global_objects.services["ritual_builder_service"]
    ritual_package = ritual_builder.build_daily_ritual()

    script = ritual_package["script"]
    mantra_loop = ritual_package["mantra_loop"]

    ritual_id = ritual_service.start_custom_ritual(ritual_type, script, mantra_loop)

    # 🔥 Instead of immediately trying to advance,
    # just return a starter message
    return RitualResponse(
        ritual_id=ritual_id,
        bot_message="Ritual started. Awaiting your first response."
    )

@router.post("/respond", response_model=RitualResponse)
def respond_ritual(request: RespondRitualRequest):
    bot_message = ritual_service.handle_response(request.ritual_id, request.user_message)
    if not bot_message:
        raise HTTPException(status_code=404, detail="Ritual session not found or already completed.")

    return RitualResponse(ritual_id=request.ritual_id, bot_message=bot_message)
