# main.py

import sys
import os
import time
import schedule
from dotenv import load_dotenv


# ✅ This forces Python to recognize /app/ as a module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now regular imports will work
from services.twilio_call_service import TwilioCallService
from services.habitica_service import HabiticaService
from services.obedience_service import ObedienceService
from services.punishment_service import PunishmentService
from services.sentiment_service import SentimentService

# (rest of your code here)

load_dotenv()

# === Initialize Services ===
twilio_service = TwilioCallService()
habitica_service = HabiticaService()
obedience_service = ObedienceService()
punishment_service = PunishmentService()
sentiment_service = SentimentService()

# === Config ===
USER_PHONE_NUMBER = os.getenv('TO_PHONE_NUMBER')  # Your phone number (E.164 format)
MORNING_CALL_TIME = "06:30"
MIDDAY_PUSH_TIME = "12:00"
EVENING_CALL_TIME = "19:33"

# === Morning Ritual ===
def morning_call_flow():
    print("🔔 Starting Morning Call Flow...")

    # 1. Pull today's dailies
    dailies = habitica_service.get_dailies()
    print(dailies)
    daily_texts = [d.get('text', 'Unnamed Task') for d in dailies]
    print(daily_texts)

    # 2. Make Morning Call
    # For MVP: Send SMS listing today's key tasks instead of real call
    body = f"Good morning! Your tasks today:\n" + "\n".join(f"- {task}" for task in daily_texts)
    print(body)
    twilio_service.send_sms(USER_PHONE_NUMBER, body)

    print("✅ Morning SMS sent with today's tasks.")

# === Midday Push (Motivation / Threat) ===
def midday_push_flow():
    print("📨 Sending Midday Nudge...")
    body = "⚡ Stay obedient! Log your habits or suffer consequences later."
    twilio_service.send_sms(USER_PHONE_NUMBER, body)
    print("✅ Midday SMS sent.")

# === Evening Ritual ===
def evening_call_flow():
    print("🌙 Starting Evening Call Flow...")

    # 1. Pull today's dailies
    dailies = habitica_service.get_dailies()

    completed = [d for d in dailies if d.get('completed', False)]
    total = len(dailies)

    success = len(completed) == total

    # 2. Update obedience
    obedience_service.update_obedience(success=success)
    punishment_level = obedience_service.get_punishment_level()

    # 3. Handle punishment if needed
    if not success:
        punishment = punishment_service.choose_punishment(punishment_level)
        habitica_service.create_punishment_task(punishment)

        body = f"⚠️ You failed your habits today.\nPunishment assigned: {punishment} (check Habitica)"
    else:
        body = "🌟 You were obedient today. No punishments assigned. Good job!"

    # 4. Evening Call (MVP = SMS first)
    twilio_service.send_sms(USER_PHONE_NUMBER, body)

    print("✅ Evening SMS sent.")

# === Schedule the Daily Flows ===
def schedule_daily_flows():
    schedule.every().day.at(MORNING_CALL_TIME).do(morning_call_flow)
    schedule.every().day.at(MIDDAY_PUSH_TIME).do(midday_push_flow)
    schedule.every().day.at(EVENING_CALL_TIME).do(evening_call_flow)

morning_call_flow()

# === Main Entry Point ===
if __name__ == "__main__":
    print("🚀 PersonalPM Enforcement Engine Starting...")
    schedule_daily_flows()

    # Main loop
    while True:
        schedule.run_pending()
        time.sleep(10)
