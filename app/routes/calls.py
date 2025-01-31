# app/routes/calls.py
from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
from app.services.twilio_service import make_call
from app.services.riddle import fetch_riddle
from app.services.calendar_service import findTodaysEvents
from app.utils.helpers import convert_iso_to_readable_time

router = APIRouter()

current_riddle = None

@router.api_route("/start-call", methods=["GET", "POST"], response_class=PlainTextResponse)
async def start_call():
    """Twilio starts the call and asks a brain teaser using Polly's voice."""
    global current_riddle

    current_riddle = fetch_riddle()
    print(current_riddle) 
    
    response = VoiceResponse()
    gather = Gather(input="speech", action="/handle-response", method="POST", timeout=5)
    
    ssml_text = (
        "<speak>"
        "<break time='500ms'/>"  # Small pause before speaking
        "Good Morning "
        "<break time='300ms'/>"
        f"{current_riddle['riddle']}"
        "</speak>"
    )

    gather.say(ssml_text)
    response.append(gather)

    return str(response)

@router.post("/handle-response", response_class=PlainTextResponse)
async def handle_response(SpeechResult: str = Form(None)):  
    """Handle user speech and say if it's right or wrong."""
    global current_riddle

    response = VoiceResponse()

    if SpeechResult is None:  # ✅ Handle silent responses
        gather = Gather(input="speech", action="/handle-response", method="POST", timeout=5)
        gather.say("I didn't hear you. Can you try answering again?")
        response.append(gather)
        return str(response)

    correct_answer = current_riddle["answer"].lower()
    user_answer = SpeechResult.lower()

    if correct_answer in user_answer:  # ✅ Allow partial matches
        response.say("That's correct! Well done!")
         # 🔹 Fetch and read today's events
        events = findTodaysEvents()

        print(events)

        if events:
            response.say("Now, here are your events for today:")
            for event in events:
                readable_time = convert_iso_to_readable_time(event["start"])
                response.say(f"{event['summary']} at {readable_time}.")
        else:
            response.say("You have no events scheduled for today.")
    else:
        gather = Gather(input="speech", action="/handle-response", method="POST", timeout=5)
        gather.say(f"Not quite! Try again. {current_riddle['riddle']}")
        response.append(gather)

    return str(response)

@router.post("/trigger-call")
async def trigger_call():
    """Start a Twilio call."""
    try:
        call_id = make_call()
        return {"status": "success", "call_id": call_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}
