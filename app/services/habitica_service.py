# /services/habitica_service.py
import os
import requests

class HabiticaService:
    def __init__(self):
        self.api_user = os.getenv('HABITICA_USER_ID')
        self.api_key = os.getenv('HABITICA_API_KEY')
        self.base_url = "https://habitica.com/api/v3"

        self.headers = {
            "x-api-user": self.api_user,
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def get_dailies(self):
        """Fetch today's dailies."""
        url = f"{self.base_url}/tasks/user?type=dailys"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return []
        
    def get_missed_count_yesterday(self):
        """Estimate missed dailies from yesterday based on due and completion status."""
        dailies = self.get_dailies()
        missed = [
            h for h in dailies
            if not h.get('completed', False) and not h.get('isDue', True)
        ]
        return len(missed)


    def create_punishment_task(self, text: str):
        """Create a punishment To-Do."""
        url = f"{self.base_url}/tasks/user"
        payload = {
            "type": "todo",
            "text": text,
            "priority": 2
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.status_code == 201
