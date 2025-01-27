from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from the .env file
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
to_number = os.getenv("TO_PHONE_NUMBER")


# Fetch events from your API
def fetch_events():
    response = requests.get(f"https://raspberrypi.local:3002/events")
    if response.status_code == 200:
        return response.json()  # Assume your API returns a list of events
    else:
        return []

# Make a call
def make_call():
    events = fetch_events()
    message = "Good morning! Here are your events for the day:\n"
    for event in events:
        message += f"- {event['summary']} at {event['start']}\n"

    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to=to_number,
        from_=twilio_phone_number,
        twiml=f"<Response><Say>{message}</Say></Response>"
    )
    print("Call scheduled successfully!")

# Schedule the call
def schedule_daily_calls():
    scheduler = BackgroundScheduler()

    # Weekday call at 6:10 AM
    scheduler.add_job(make_call, 'cron', day_of_week='mon-fri', hour=6, minute=10)

    # Weekend call at 8:10 AM
    scheduler.add_job(make_call, 'cron', day_of_week='sat,sun', hour=8, minute=10)

    scheduler.start()
    print("Scheduler started!")

# Run the scheduler
if __name__ == "__main__":
    schedule_daily_calls()
    try:
        # Keep the script running
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        print("Stopping the scheduler...")
