# app/routes/calls.py
import os
from fastapi import APIRouter, Form, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
from app.services.calendar_service import findTodaysEvents
from app.services.conversation_manager import ConversationManager
from app.utils.helpers import convert_iso_to_readable_time
from app.config import OPENAI_API_KEY

router = APIRouter()

current_riddle = None


conv_manager = ConversationManager(
    api_key=OPENAI_API_KEY,
)


@router.post("/voice")
async def voice(request: Request):
    form_data = await request.form()
    # Twilio will post either SpeechResult (from speech recognition) or Digits.
    user_input = form_data.get("SpeechResult") or form_data.get("Digits", "")

    twilio_response = VoiceResponse()
    # Use <Gather> to prompt for voice input. The 'action' attribute loops back to this endpoint.
    gather = Gather(input="speech", action="/voice", speechTimeout="auto")

    if conv_manager.conversation_history == "":
        # First turn: initiate conversation using custom JSON for a dynamic starter.
        initial_message = conv_manager.initiate_conversation()
        gather.say(initial_message)
    else:
        # Subsequent turns: process the user's input and continue the conversation.
        generated_response = conv_manager.continue_conversation(user_input)
        gather.say(generated_response)

    twilio_response.append(gather)
    return PlainTextResponse(str(twilio_response), media_type="application/xml")


@router.post("/trigger-call")
async def trigger_call():
    """Start a Twilio call."""
    try:
        call_id = make_call()
        return {"status": "success", "call_id": call_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}
