# test_twilio.py

import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables
load_dotenv()

# Twilio setup
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_number = os.getenv('TWILIO_PHONE_NUMBER')
to_number = os.getenv('USER_PHONE_NUMBER')

client = Client(account_sid, auth_token)

# Send test SMS
message = client.messages.create(
    body="🚀 Test SMS from PersonalPM!",
    from_=from_number,
    to=to_number
)

print(f"✅ Test Message SID: {message.sid}")
