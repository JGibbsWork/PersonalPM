# /managers/evening_manager.py

from datetime import datetime

class EveningManager:
    def __init__(self, habitica_service, obedience_service, punishment_service, tone_service,
                 failure_tracker_service, escalation_manager_service, obedience_lockdown_manager):
        self.habitica_service = habitica_service
        self.obedience_service = obedience_service
        self.punishment_service = punishment_service
        self.tone_service = tone_service
        self.failure_tracker_service = failure_tracker_service
        self.escalation_manager_service = escalation_manager_service
        self.obedience_lockdown_manager = obedience_lockdown_manager

    def build_context_payload(self) -> dict:
        """Build the full context payload for an evening ritual conversation."""

        # Pull today's habits/dailies
        habits = self.habitica_service.get_dailies()
        if not habits:
            habits = []

        # Check which habits were missed
        missed_habits = [habit.get('text', 'Unnamed Habit') for habit in habits if not habit.get('completed', False)]

        # Update obedience based on habits completed
        success = len(missed_habits) == 0
        self.obedience_service.update_obedience(success=success)

        # 🛠️ Track failure if disobedient
        if not success:
            self.failure_tracker_service.record_failure()

        # Pull updated obedience score
        obedience_score = self.obedience_service.get_current_obedience_score()

        # Get tone (mean if disobedient, softer if obedient)
        tone = self.tone_service.get_tone_based_on_obedience()

        # Handle escalation path if needed
        violation = "Failed to complete daily obligations."
        preferences = ["physical", "mental", "lifestyle"]  # Could dynamically load user preferences here

        punishment_or_lockdown = self.escalation_manager_service.check_and_escalate(
            violation=violation,
            preferences=preferences
        )

        if punishment_or_lockdown == "FULL_LOCKDOWN":
            print("🔒 Triggering FULL OBEDIENCE LOCKDOWN.")
            self.obedience_lockdown_manager.assign_lockdown_day()
            punishment_task = "FULL_OBEDIENCE_LOCKDOWN_ASSIGNED"
        else:
            punishment_task = punishment_or_lockdown
            if punishment_task:
                self.habitica_service.create_punishment_task(punishment_task)

        # Build the full context payload
        context_payload = {
            "time_of_day": "evening",
            "ritual": "daily review and punishment",
            "tone": tone,
            "missed_habits": missed_habits,
            "obedience_score": obedience_score,
            "punishment_task": punishment_task,
            "date_today": datetime.now().strftime("%A, %B %d, %Y"),
            "daily_failures": self.failure_tracker_service.get_daily_failures(),
            "weekly_failures": self.failure_tracker_service.get_weekly_failures()
        }

        return context_payload
