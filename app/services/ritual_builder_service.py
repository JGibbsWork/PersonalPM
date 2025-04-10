# /services/ritual_builder_service.py

class RitualBuilderService:
    def build_daily_ritual(self) -> dict:
        return {
            "script": [
                {"action": "check_habits"},
                {"action": "confirm_tasks"},
                {"action": "calendar_review"},
                {"action": "assign_punishments"},
                {"action": "dismissal"}
            ],
            "mantra_loop": {
                "mantra_text": "With clarity and purpose, I serve dutifully and with gratitude.",
                "target_repetitions": 5,
                "current_repetitions": 0
            }
        }
