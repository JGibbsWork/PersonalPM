# /managers/morning_ritual_manager.py

import random
from datetime import datetime

class MorningRitualManager:
    def __init__(self, obedience_service, habitica_service, calendar_service):
        self.obedience_service = obedience_service
        self.habitica_service = habitica_service
        self.calendar_service = calendar_service

        # Example mantras - you can expand this!
        self.mantras = [
            "Discipline is freedom. I choose discipline.",
            "Today, I will conquer through my actions.",
            "Obedience is strength. Resistance is weakness.",
            "My rituals define my destiny."
        ]

    def get_today_mantra(self):
        return random.choice(self.mantras)

    def get_today_calendar_events(self):
        # Placeholder
        events = self.calendar_service.get_today_events()
        if not events:
            return "You have no scheduled events today."
        event_texts = [f"At {event['start_time']}, {event['title']}" for event in events]
        return "Here are your key events for today: " + "; ".join(event_texts)

    def get_today_habit_reminders(self):
        dailies = self.habitica_service.get_dailies()
        if not dailies:
            return "No habit reminders for today."
        daily_texts = [d.get('text', 'Unnamed Habit') for d in dailies]
        return "Remember your key habits today: " + "; ".join(daily_texts)

    def build_morning_script(self):
        # Dynamic tone adjustment
        punishment_level = self.obedience_service.get_punishment_level()

        if punishment_level == "light":
            tone_intro = "Good morning. You have been obedient. Continue your focus."
        elif punishment_level == "medium":
            tone_intro = "Attention. Your obedience is slipping. Focus harder."
        else:
            tone_intro = "You have disobeyed. Redemption requires action today."

        # Build the full script
        script = f"""
{tone_intro}

Mantra of the day:
{self.get_today_mantra()}

{self.get_today_calendar_events()}

{self.get_today_habit_reminders()}

Proceed with discipline.
"""
        return script.strip()
