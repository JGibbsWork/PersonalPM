from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from the .env file
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
to_number = os.getenv("TO_PHONE_NUMBER")

# Create a Twilio client
client = Client(account_sid, auth_token)

# Function to make a call
def make_call(message_url):
    try:
        call = client.calls.create(
            to=to_number,  # Recipient's phone number
            from_=twilio_phone_number,  # Your Twilio number
            url="http://demo.twilio.com/docs/voice.xml"
            )
        print(f"Call initiated! Call SID: {call.sid}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
message_url = "http://demo.twilio.com/docs/voice.xml"  # Replace with your TwiML URL
make_call(message_url)
