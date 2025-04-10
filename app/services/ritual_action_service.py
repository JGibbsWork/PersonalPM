# /services/ritual_action_service.py

from shared import global_objects

class RitualActionService:
    def __init__(self):
        pass  # 🛡️ No service grabbing here!

    def check_habits(self):
        habitica_service = global_objects.services["habitica_service"]
        missed_count = habitica_service.get_missed_count_yesterday()

        if missed_count == 0:
            return "Good. You completed all your tasks yesterday. Well done."
        else:
            return f"You missed {missed_count} tasks yesterday. Your discipline is lacking."


    def confirm_tasks(self):
        habitica_service = global_objects.services["habitica_service"]
        dailies = habitica_service.get_dailies()
        dailies_list = ", ".join(h['text'] for h in dailies)
        return f"Recite today's duties out loud: {dailies_list}."

    def calendar_review(self):
        calendar_service = global_objects.services["calendar_service"]
        events = calendar_service.get_today_events()
        if not events:
            return "No scheduled events today. You have no excuses."
        else:
            event_list = ", ".join(f"{e.get('summary', 'Unnamed Event')} at {e.get('start', 'Unknown time')}" for e in events)
            return f"Today's obligations are: {event_list}."


    def assign_punishments(self):
        habitica_service = global_objects.services["habitica_service"]
        punishment_selector_service = global_objects.services["punishment_selector_service"]

        missed_count = habitica_service.get_missed_count_yesterday()
        if missed_count > 0:
            punishment = punishment_selector_service.choose_punishment(level="medium")
            habitica_service.create_punishment_task(punishment)
            return f"Punishment assigned: {punishment}. Complete it without failure."
        else:
            return "No punishments today. Stay obedient."

    def dismissal(self):
        return "Ritual complete. Serve with strength and precision today."
