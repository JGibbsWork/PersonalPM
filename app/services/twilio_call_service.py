# /services/twilio_call_service.py
from twilio.rest import Client
import os

class TwilioCallService:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.client = Client(self.account_sid, self.auth_token)

    def make_call(self, to_number: str, twiml_url: str):
        """Place a call to the user with a given TwiML URL."""
        call = self.client.calls.create(
            to=to_number,
            from_=self.from_number,
            url=twiml_url
        )
        return call.sid

    def send_sms(self, to_number: str, body: str):
        """Send an SMS to the user."""
        message = self.client.messages.create(
            to=to_number,
            from_=self.from_number,
            body=body
        )
        return message.sid
