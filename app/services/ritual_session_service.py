# /services/ritual_session_service.py

import uuid
from typing import Dict

class RitualSessionService:
    def __init__(self):
        self.active_rituals: Dict[str, dict] = {}

    def start_custom_ritual(self, ritual_type: str, opening_line: str):
        ritual_id = str(uuid.uuid4())
        script = [opening_line]
        self.active_rituals[ritual_id] = {
            "script": script,
            "current_index": 0,
            "type": ritual_type
        }
        return ritual_id

    def handle_response(self, ritual_id: str, user_message: str):
        ritual = self.active_rituals.get(ritual_id)
        if not ritual:
            return None

        # Advance conversation — TODO: you can expand this with smarter dialogue later
        ritual["current_index"] += 1
        idx = ritual["current_index"]

        if idx < len(ritual["script"]):
            return ritual["script"][idx]
        else:
            # Ritual complete
            del self.active_rituals[ritual_id]
            return "Ritual complete. You have been judged."

# Instantiate singleton
ritual_service = RitualSessionService()
