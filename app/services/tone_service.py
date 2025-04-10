# /services/tone_service.py

class ToneService:
    def __init__(self):
        pass

    def get_tone_based_on_obedience(self, obedience_score: int) -> str:
        """
        Decide tone based on obedience score.
        Higher score = softer tone, lower score = more brutal.
        """
        if obedience_score >= 80:
            return "encouraging"
        elif obedience_score >= 50:
            return "neutral"
        else:
            return "aggressive"
