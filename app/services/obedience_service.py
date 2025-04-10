# /services/obedience_service.py

class ObedienceService:
    def __init__(self):
        self.success_days = 0
        self.failure_days = 0
        self.current_punishment_level = "light"

    def update_obedience(self, success: bool):
        """Update success/failure counters and punishment severity."""
        if success:
            self.success_days += 1
            self.failure_days = 0
            self.current_punishment_level = "light"
        else:
            self.failure_days += 1
            self.success_days = 0
            if self.failure_days == 1:
                self.current_punishment_level = "light"
            elif self.failure_days == 2:
                self.current_punishment_level = "medium"
            else:
                self.current_punishment_level = "heavy"

    def get_punishment_level(self):
        return self.current_punishment_level
