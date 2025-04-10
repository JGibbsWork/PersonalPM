# /app/main.py

import os
import time
import schedule
from dotenv import load_dotenv

# === Load env vars ===
load_dotenv()

# === Services ===
from services.habitica_service import HabiticaService
from services.obedience_service import ObedienceService
from services.punishment_service import PunishmentService
from services.mantra_service import MantraService
from services.twilio_call_service import TwilioCallService
from services.sentiment_service import SentimentService
from services.penance_service import PenanceService
from services.punishment_selector_service import PunishmentSelectorService
from services.calendar_service import findTodaysEvents
from services.tone_service import ToneService
from services.failure_tracker_service import FailureTrackerService
from services.escalation_manager_service import EscalationManagerService
from services.obedience_lockdown_manager import ObedienceLockdownManager
from services.punishment_context_processor import PunishmentContextProcessor
from services.punishment_generator_service import PunishmentGeneratorService

# === Managers ===
from managers.morning_manager import MorningManager
from managers.midday_manager import MiddayManager
from managers.evening_manager import EveningManager
from managers.conversation_manager import ConversationManager

# === Initialize services ===
habitica_service = HabiticaService()
obedience_service = ObedienceService()
punishment_service = PunishmentService()
mantra_service = MantraService()
twilio_service = TwilioCallService()
sentiment_service = SentimentService()
punishment_selector_service = PunishmentSelectorService()
penance_service = PenanceService(habitica_service=habitica_service, punishment_selector_service=punishment_selector_service)
calendar_service = findTodaysEvents
tone_service = ToneService()
failure_tracker_service = FailureTrackerService()
punishment_context_processor = PunishmentContextProcessor()

raw_punishment_notes = """
Your full dump of punishment philosophy text goes here — for MVP you can use a small sample.
"""
punishment_doctrine = punishment_context_processor.process_raw_notes(raw_punishment_notes)


punishment_generator_service = PunishmentGeneratorService(punishment_doctrine)


escalation_manager_service = EscalationManagerService(
    punishment_generator_service=punishment_generator_service,
    failure_tracker_service=failure_tracker_service,
    penance_service=penance_service
)

obedience_lockdown_manager = ObedienceLockdownManager(habitica_service=habitica_service)


# === Initialize managers ===
morning_manager = MorningManager(
    habitica_service=habitica_service,
    calendar_service=calendar_service,
    obedience_service=obedience_service,
    mantra_service=mantra_service,
    tone_service=tone_service
)

midday_manager = MiddayManager(
    habitica_service=habitica_service,
    obedience_service=obedience_service,
    tone_service=tone_service
)

evening_manager = EveningManager(
    habitica_service=habitica_service,
    obedience_service=obedience_service,
    punishment_service=punishment_selector_service,
    tone_service=tone_service,
    failure_tracker_service=failure_tracker_service,
    escalation_manager_service=escalation_manager_service,
    obedience_lockdown_manager=obedience_lockdown_manager
)

conversation_manager = ConversationManager()

# === Config ===
USER_PHONE_NUMBER = os.getenv('USER_PHONE_NUMBER')
MORNING_CALL_TIME = "06:30"
MIDDAY_PUSH_TIME = "12:00"
EVENING_CALL_TIME = "19:30"

# === Daily Ritual Flows ===

def morning_ritual_flow():
    print("🌅 Morning Ritual Starting...")
    context_payload = morning_manager.build_context_payload()
    starter_message = conversation_manager.initiate_conversation(context_payload)
    twilio_service.send_sms(USER_PHONE_NUMBER, starter_message)
    print("✅ Morning Ritual Complete.")

def midday_motivation_flow():
    print("🏋️ Midday Motivation Push...")
    context_payload = midday_manager.build_context_payload()
    starter_message = conversation_manager.initiate_conversation(context_payload)
    twilio_service.send_sms(USER_PHONE_NUMBER, starter_message)
    print("✅ Midday Motivation Sent.")

def evening_ritual_flow():
    print("🌙 Evening Ritual Starting...")
    context_payload = evening_manager.build_context_payload()
    starter_message = conversation_manager.initiate_conversation(context_payload)
    
    twilio_service.send_sms(USER_PHONE_NUMBER, starter_message)

    print("✅ Evening Ritual Complete.")

# === Scheduling the Rituals ===

def schedule_daily_flows():
    schedule.every().day.at(MORNING_CALL_TIME).do(morning_ritual_flow)
    schedule.every().day.at(MIDDAY_PUSH_TIME).do(midday_motivation_flow)
    schedule.every().day.at(EVENING_CALL_TIME).do(evening_ritual_flow)

# === Entry Point ===

if __name__ == "__main__":
    print("🚀 PersonalPM Enforcement Engine Starting...")
    schedule_daily_flows()

    while True:
        schedule.run_pending()
        time.sleep(10)
