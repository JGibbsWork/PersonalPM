# /services/penance_service.py

import datetime

class PenanceService:
    def __init__(self, habitica_service, punishment_selector_service):
        self.habitica_service = habitica_service
        self.punishment_selector_service = punishment_selector_service
        self.active_penance_task_id = None
        self.active_due_datetime = None

    def assign_penance_task(self, violation: str, preferences: list) -> str:
        """Assign a penance task and set a hard due time."""

        # Pick or generate a penance task
        penance_text = self.punishment_selector_service.choose_penance_task(violation, preferences)

        # Create it in Habitica
        task_id = self.habitica_service.create_punishment_task(penance_text)

        # Set task tracking
        self.active_penance_task_id = task_id
        self.active_due_datetime = datetime.datetime.now() + datetime.timedelta(hours=24)  # 24-hour completion window

        return penance_text

    def check_penance_completion(self) -> bool:
        """Check if the penance task is completed and on time."""
        if not self.active_penance_task_id:
            return False  # No active penance

        task = self.habitica_service.get_task_by_id(self.active_penance_task_id)
        if task and task.get('completed', False):
            # Check if completed on time
            completed_time = datetime.datetime.now()  # (Optionally: pull real task completedAt if Habitica returns it)
            if completed_time <= self.active_due_datetime:
                self._clear_penance()
                return True
            else:
                print("⏰ Penance task completed but LATE.")
                return False

        # Task not completed
        if datetime.datetime.now() > self.active_due_datetime:
            print("🚨 Penance task overdue and NOT completed.")
            return False

        return False  # Not completed yet but still within window

    def _clear_penance(self):
        """Clear penance task tracking."""
        self.active_penance_task_id = None
        self.active_due_datetime = None

    def has_active_penance(self) -> bool:
        return self.active_penance_task_id is not None
