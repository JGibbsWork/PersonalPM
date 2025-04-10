# /initializers/service_initializer.py

from services.calendar_service import CalendarService
from services.mantra_service import MantraService
from services.habitica_service import HabiticaService
from services.obedience_service import ObedienceService
from services.sentiment_service import SentimentService
from services.tone_service import ToneService
from services.punishment_context_processor import PunishmentContextProcessor
from services.punishment_generator_service import PunishmentGeneratorService
from services.punishment_selector_service import PunishmentSelectorService
from services.penance_service import PenanceService
from services.failure_tracker_service import FailureTrackerService
from services.escalation_manager_service import EscalationManagerService
from services.obedience_lockdown_manager import ObedienceLockdownManager
from services.ritual_script_generator_service import RitualScriptGeneratorService
from services.ritual_session_service import RitualSessionService
from services.ritual_builder_service import RitualBuilderService


def initialize_services(punishment_doctrine):
    habitica_service = HabiticaService()
    obedience_service = ObedienceService()
    sentiment_service = SentimentService()
    tone_service = ToneService()
    punishment_selector_service = PunishmentSelectorService()
    punishment_generator_service = PunishmentGeneratorService(punishment_doctrine)
    penance_service = PenanceService(habitica_service, punishment_selector_service)
    failure_tracker_service = FailureTrackerService()
    escalation_manager_service = EscalationManagerService(
        punishment_generator_service, failure_tracker_service, penance_service
    )
    obedience_lockdown_manager = ObedienceLockdownManager(habitica_service)
    mantra_service=MantraService()
    calendar_service = CalendarService()
    ritual_script_generator_service = RitualScriptGeneratorService()
    ritual_session_service = RitualSessionService()
    ritual_builder_service = RitualBuilderService()

    return {
        "habitica_service": habitica_service,
        "obedience_service": obedience_service,
        "sentiment_service": sentiment_service,
        "tone_service": tone_service,
        "punishment_selector_service": punishment_selector_service,
        "punishment_generator_service": punishment_generator_service,
        "penance_service": penance_service,
        "failure_tracker_service": failure_tracker_service,
        "escalation_manager_service": escalation_manager_service,
        "obedience_lockdown_manager": obedience_lockdown_manager,
        "calendar_service": calendar_service,
        "mantra_service": mantra_service,
        "ritual_script_generator_service": ritual_script_generator_service,
        "ritual_session_service": ritual_session_service,
        "ritual_builder_service": ritual_builder_service
    }
