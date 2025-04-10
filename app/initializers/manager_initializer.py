# /initializers/manager_initializer.py

from managers.evening_manager import EveningManager
from managers.morning_manager import MorningManager
from managers.midday_manager import MiddayManager
from managers.conversation_manager import ConversationManager

def initialize_managers(services):
    morning_manager = MorningManager(
        habitica_service=services["habitica_service"],
        calendar_service=services["calendar_service"], 
        obedience_service=services["obedience_service"],
        mantra_service=services["mantra_service"],  # TEMP: Swap to real mantra service later
        tone_service=services["tone_service"]
    )

    midday_manager = MiddayManager(
        habitica_service=services["habitica_service"],
        obedience_service=services["obedience_service"],
        tone_service=services["tone_service"]
    )

    evening_manager = EveningManager(
        habitica_service=services["habitica_service"],
        obedience_service=services["obedience_service"],
        punishment_service=services["punishment_selector_service"],
        tone_service=services["tone_service"],
        failure_tracker_service=services["failure_tracker_service"],
        escalation_manager_service=services["escalation_manager_service"],
        obedience_lockdown_manager=services["obedience_lockdown_manager"]
    )

    conversation_manager = ConversationManager()

    return {
        "morning_manager": morning_manager,
        "midday_manager": midday_manager,
        "evening_manager": evening_manager,
        "conversation_manager": conversation_manager
    }

