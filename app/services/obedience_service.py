# /services/obedience_service.py

class ObedienceService:
    def __init__(self):
        self.obedience_score = 100  # Starting score
        self.success_days = 0
        self.failure_days = 0
        self.current_punishment_level = "light"

    def update_obedience(self, success: bool):
        """Updates obedience based on daily behavior."""
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

    def get_current_obedience_score(self):
        return self.obedience_score

    def get_punishment_level(self):
        return self.current_punishment_level

    def reward_for_respect(self):
        """Slight boost for polite/submissive behavior."""
        self.obedience_score = min(self.obedience_score + 2, 100)

    def penalize_minor_disrespect(self):
        """Mild penalty for mild disrespect."""
        self.obedience_score = max(self.obedience_score - 5, 0)

    def penalize_major_disobedience(self):
        """Stronger penalty for refusal or resistance."""
        self.obedience_score = max(self.obedience_score - 10, 0)

    def penalize_severe_disobedience(self):
        """Harsh penalty for open rebellion."""
        self.obedience_score = max(self.obedience_score - 20, 0)

    def offer_forgiveness(self):
        """Offer mercy: increase obedience slightly, soften punishment level."""
        self.obedience_score = min(self.obedience_score + 10, 100)

        # Soften punishment if possible
        if self.current_punishment_level == "heavy":
            self.current_punishment_level = "medium"
        elif self.current_punishment_level == "medium":
            self.current_punishment_level = "light"
