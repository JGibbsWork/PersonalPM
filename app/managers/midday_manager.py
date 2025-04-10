# /managers/midday_manager.py

import random
from datetime import datetime

class MiddayManager:
    def __init__(self, habitica_service, obedience_service, tone_service):
        self.habitica_service = habitica_service
        self.obedience_service = obedience_service
        self.tone_service = tone_service

    def build_context_payload(self) -> dict:
        """Build the full context payload for a random midday intervention."""

        # Pull obedience standing
        obedience_score = self.obedience_service.get_current_obedience_score()

        # Pull habits (dailies)
        habits = self.habitica_service.get_dailies()
        incomplete_habits = [habit.get('text', 'Unnamed Habit') for habit in habits if not habit.get('completed', False)]

        # Get tone
        tone = self.tone_service.get_tone_based_on_obedience()

        # Pick random attack type
        attack_type = random.choice(["habit_check", "obedience_reminder", "random_threat"])

        # Build context based on attack type
        if attack_type == "habit_check":
            message_type = "habit check"
            focus_habit = random.choice(incomplete_habits) if incomplete_habits else "stay disciplined"
            custom_message = f"Check if you completed: {focus_habit}"
        
        elif attack_type == "obedience_reminder":
            message_type = "obedience score reminder"
            custom_message = f"Your current obedience score is {obedience_score}%. Stay fucking sharp."
        
        else:  # random threat
            message_type = "random threat"
            custom_message = "If you fuck around today, you'll pay double tonight. Stay locked in."

        context_payload = {
            "time_of_day": "midday",
            "ritual": message_type,
            "tone": tone,
            "message": custom_message,
            "date_today": datetime.now().strftime("%A, %B %d, %Y"),
            "obedience_score": obedience_score,
            "incomplete_habits": incomplete_habits
        }

        return context_payload
