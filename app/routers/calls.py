import os
from app.services.twilio_service import make_call
from fastapi import APIRouter, Request, Response
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
from app.services.conversation_manager import ConversationManager
from app.services.mantra_service import MantraService
import random

router = APIRouter()
mantra_service = MantraService()

router = APIRouter()

conv_manager = ConversationManager()

@router.get("/")
async def index():
    return {"message": "Hello, World!"}

@router.post("/voice")
async def voice(request: Request):
    print("Received Twilio request")
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

@router.get("/trigger-call")
async def trigger_call():
    mantra, repetitions = mantra_service.generate_mantra()

    response = VoiceResponse()
    
    response.say("Wake up, pet. Listen carefully.", voice='Polly.Matthew', language='en-US')
    response.say(f"Repeat after me: {mantra}", voice='Polly.Matthew', language='en-US')

    gather = Gather(
        input='speech',
        timeout=5,
        speech_timeout='auto',
        action=f"/voice/repeat?mantra={mantra}&reps_left={repetitions}",
        method="POST"
    )
    gather.say("Say it now.", voice='Polly.Matthew', language='en-US')
    response.append(gather)

    return Response(content=str(response), media_type="application/xml")

@router.post("/voice/repeat")
async def repeat(request: Request):
    form = await request.form()
    speech_result = form.get("SpeechResult", "").lower()

    mantra = request.query_params.get("mantra", "").lower()
    reps_left = int(request.query_params.get("reps_left", 0))

    # Clean speech and mantra
    cleaned_speech = speech_result.strip().lower().replace(".", "").replace(",", "")
    cleaned_mantra = mantra.strip().lower().replace(".", "").replace(",", "")

    response = VoiceResponse()

    if cleaned_mantra in cleaned_speech:
        reps_left -= 1

        if reps_left <= 0:
            response.say("Good. Now receive your instructions.", voice='Polly.Matthew', language='en-US')
            response.redirect("/voice/summary")
            return Response(content=str(response), media_type="application/xml")
        else:
            # Say something BEFORE gathering again
            repeat_phrases = [
                "Again.",
                "Repeat it.",
                "Say it once more.",
                "Another time, pet.",
                "You will say it again, without hesitation."
            ]
            phrase = random.choice(repeat_phrases)
            response.say(phrase, voice='Polly.Matthew', language='en-US')

            gather = Gather(
                input='speech',
                timeout=5,
                speech_timeout='auto',
                action=f"/voice/repeat?mantra={mantra}&reps_left={reps_left}",
                method="POST"
            )
            gather.say("Say it now.", voice='Polly.Matthew', language='en-US')
            response.append(gather)

            return Response(content=str(response), media_type="application/xml")
    else:
        gather = Gather(
            input='speech',
            timeout=5,
            speech_timeout='auto',
            action=f"/voice/repeat?mantra={mantra}&reps_left={reps_left}",
            method="POST"
        )
        response.say("Incorrect. The mantra is:", voice='Polly.Matthew', language='en-US')
        response.say(f"{mantra}", voice='Polly.Matthew', language='en-US')
        gather.say("Say it now.", voice='Polly.Matthew', language='en-US')
        response.append(gather)

        return Response(content=str(response), media_type="application/xml")
            

@router.post("/voice/summary")
async def summary():
    response = VoiceResponse()
    response.say("Today's tasks: Workout. Eat correctly. Confirm chastity. No failures tolerated.", voice='Polly.Matthew', language='en-US')
    response.say("Now go.", voice='Polly.Matthew', language='en-US')
    return Response(content=str(response), media_type="application/xml")

