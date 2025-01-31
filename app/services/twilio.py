from twilio.rest import Client

TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_number"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

async def send_sms(message: str, to: str):
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=to,
    )
