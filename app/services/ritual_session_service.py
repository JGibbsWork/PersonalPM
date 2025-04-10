import uuid
import random
from typing import Dict
from rapidfuzz import fuzz
from services.ritual_action_service import RitualActionService

class RitualSessionService:
    def __init__(self):
        self.active_rituals: Dict[str, dict] = {}
        self.action_service = RitualActionService()

    def start_custom_ritual(self, ritual_type: str, script: list, mantra_loop: dict = None):
        ritual_id = str(uuid.uuid4())
        self.active_rituals[ritual_id] = {
            "script": script,
            "current_index": -1,  # Start before first message
            "type": ritual_type,
            "mantra_loop": mantra_loop
        }
        return ritual_id

    def handle_response(self, ritual_id: str, user_message: str):
        ritual = self.active_rituals.get(ritual_id)
        if not ritual:
            return None

        # Handle mantra loop
        mantra_loop = ritual.get("mantra_loop")
        if mantra_loop and mantra_loop["current_repetitions"] < mantra_loop["target_repetitions"]:
            mantra_text = mantra_loop["mantra_text"]

            if mantra_loop["current_repetitions"] == 0:
                mantra_loop["current_repetitions"] += 1
                return f"Your mantra today is: '{mantra_text}'. Say it now."

            # User must repeat mantra correctly
            cleaned_user_message = user_message.strip().lower()
            similarity = fuzz.ratio(cleaned_user_message.lower(), mantra_text.lower())

            if similarity >= 85:
                # Correct repetition
                mantra_loop["current_repetitions"] += 1
                if mantra_loop["current_repetitions"] > mantra_loop["target_repetitions"]:
                    return "Good. Proceeding to your duties."
                else:
                    return random.choice([
                        "Again.",
                        "One more time.",
                        "Say it louder.",
                        "With more devotion.",
                        "Repeat perfectly."
                    ])
            else:
                # Incorrect repetition — scold, don't increment counter
                return random.choice([
                    "No, that wasn't it. Try again.",
                    "Incorrect. Focus and say it properly.",
                    "Wrong. Repeat it exactly.",
                    "You will not move on until you say it right."
                ])

        # Handle normal ritual flow
        ritual["current_index"] += 1
        idx = ritual["current_index"]

        if idx < len(ritual["script"]):
            step = ritual["script"][idx]
            action = step.get("action")

            # 🔥 Route to appropriate Action Service method
            if action == "check_habits":
                return self.action_service.check_habits()
            elif action == "confirm_tasks":
                return self.action_service.confirm_tasks()
            elif action == "calendar_review":
                return self.action_service.calendar_review()
            elif action == "assign_punishments":
                return self.action_service.assign_punishments()
            elif action == "dismissal":
                return self.action_service.dismissal()
            else:
                return "Unknown ritual step."
        else:
            del self.active_rituals[ritual_id]
            return "Ritual complete. Serve properly."

# 🔥 ADD THIS AT THE BOTTOM!!!
ritual_service = RitualSessionService()