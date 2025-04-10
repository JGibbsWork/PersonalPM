# /managers/morning_manager.py

from datetime import datetime

class MorningManager:
    def __init__(self, habitica_service, calendar_service, obedience_service, mantra_service, tone_service):
        self.habitica_service = habitica_service
        self.calendar_service = calendar_service
        self.obedience_service = obedience_service
        self.mantra_service = mantra_service
        self.tone_service = tone_service

    def build_context_payload(self) -> dict:
        """Build the full context payload for a morning ritual conversation."""

        # Pull today's events
        events = self.calendar_service.get_today_events()  # Should return list of {summary, start_time}
        if not events:
            events = []

        # Pull today's habits/dailies
        habits = self.habitica_service.get_dailies()  # Should return list of {text} or similar
        if not habits:
            habits = []

        # Pull obedience standing
        obedience_score = self.obedience_service.get_current_obedience_score()

        # Pull mantra
        mantra, repetitions = self.mantra_service.generate_mantra()

        # Pull tone (friendly if high obedience, harsh if low)
        obedience_score = self.obedience_service.get_current_obedience_score()
        tone = self.tone_service.get_tone_based_on_obedience(obedience_score)


        # Build the payload
        context_payload = {
            "time_of_day": "morning",
            "ritual": "daily_start",
            "tone": tone,
            "mantra": mantra,
            "calendar_events": [
                {"summary": event.get('summary', 'Unnamed Event'), "start": event.get('start_time', 'Unknown Time')}
                for event in events
            ],
            "habit_reminders": [
                habit.get('text', 'Unnamed Habit') for habit in habits
            ],
            "obedience_score": obedience_score,
            "date_today": datetime.now().strftime("%A, %B %d, %Y")
        }

        return context_payload
