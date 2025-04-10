# /services/obedience_lockdown_manager.py

class ObedienceLockdownManager:
    def __init__(self, habitica_service):
        self.habitica_service = habitica_service

    def assign_lockdown_day(self):
        """
        Assign full-day lockdown tasks to the user.
        """
        lockdown_tasks = [
            "No phone or screens allowed except alarms.",
            "Complete 300 burpees spread throughout the day.",
            "Write a 1000-word reflection: 'Why I Need Structure and Discipline.'",
            "Bedtime strictly enforced: 8:00 PM sharp. Photo proof required.",
            "Restricted speech: Only 'Yes, Sir' or 'No, Sir' responses for 24 hours."
        ]

        for task_text in lockdown_tasks:
            self.habitica_service.create_punishment_task(task_text)

        print("🔒 FULL LOCKDOWN tasks assigned in Habitica.")
