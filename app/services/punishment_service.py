# /services/punishment_service.py

class PunishmentService:
    def __init__(self):
        self.punishment_tiers = {
            "light": [
                "Do 10 push-ups",
                "Take a 5-minute cold shower",
                "Walk 1 mile"
            ],
            "medium": [
                "Do 50 push-ups",
                "Take a 10-minute cold shower",
                "Deep clean your kitchen"
            ],
            "heavy": [
                "Do 100 burpees",
                "Take a 30-minute cold shower",
                "Write 1000 words of self-critique"
            ]
        }

    def choose_punishment(self, severity: str):
        """Choose a punishment based on current severity."""
        import random
        return random.choice(self.punishment_tiers.get(severity, []))
