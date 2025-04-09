# app/twilio/twilio_helper.py

from twilio.twiml.voice_response import VoiceResponse, Gather

def build_say(text, voice="Polly.Matthew", language="en-US"):
    response = VoiceResponse()
    response.say(text, voice=voice, language=language)
    return response

def build_gather(action_url, prompt_text="Say it now.", voice="Polly.Matthew", language="en-US"):
    response = VoiceResponse()
    gather = Gather(
        input='speech',
        timeout=5,
        speech_timeout='auto',
        action=action_url,
        method="POST"
    )
    gather.say(prompt_text, voice=voice, language=language)
    response.append(gather)
    return response

def build_redirect(url):
    response = VoiceResponse()
    response.redirect(url)
    return response
