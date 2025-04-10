# /services/punishment_selector_service.py

import openai
import os

class PunishmentSelectorService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # Static punishment catalog grouped by categories
        self.punishment_catalog = {
            "physical": [
                "Do 50 push-ups.",
                "Run 1 mile without stopping.",
                "Perform 100 burpees immediately."
            ],
            "mental": [
                "Write a 500-word essay on obedience.",
                "Spend 30 minutes meditating on self-discipline.",
                "Write a detailed reflection on why you failed today."
            ],
            "lifestyle": [
                "No screens after 6 PM today.",
                "Delete entertainment apps from your phone for 24h.",
                "Deep clean your living space for 2 continuous hours."
            ],
            "financial": [
                "Donate $5 to a political cause you dislike.",
                "Donate $20 to a punishment charity.",
                "Cancel one monthly subscription you enjoy."
            ]
        }

    def choose_punishment(self, violation: str, severity: str, preferences: list, past_punishments: list) -> str:
        """Use LLM to intelligently select an appropriate punishment."""

        prompt = f"""
You are an intelligent punishment selector for a behavioral enforcement system.

User context:
- Violation: {violation}
- Severity: {severity}
- Preferences: {", ".join(preferences)}
- Past punishments recently given: {", ".join(past_punishments)}

Punishment Catalog:
{self.punishment_catalog}

Your job:
- Select ONE punishment that fits the severity level and the user's preferred punishment types.
- Avoid repeating punishments from the recent punishment history.
- Make sure the punishment is appropriately harsh based on severity and violation.
- Respond ONLY with the punishment text from the catalog (no extra commentary).

Which punishment do you assign?
"""

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You assign punishments for disobedience and disrespect."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=100,
        )

        punishment = response['choices'][0]['message']['content'].strip()
        return punishment
