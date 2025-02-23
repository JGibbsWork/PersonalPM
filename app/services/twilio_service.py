# app/services/twilio_service.py
from twilio.rest import Client
from app.config import TWILIO_ACCOUNT_SID, TWILIO_TOKEN, TWILIO_PHONE_NUMBER, TO_PHONE_NUMBER, NGROK_URL

client = Client(TWILIO_ACCOUNT_SID, TWILIO_TOKEN)

def make_call():
    print(TWILIO_PHONE_NUMBER, TO_PHONE_NUMBER, NGROK_URL)
    """Initiate a Twilio call and direct to the call flow."""
    call = client.calls.create(
        to=TO_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        url=NGROK_URL + "/voice"
    )
    return call.sid