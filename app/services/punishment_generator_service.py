# /services/punishment_generator_service.py

import openai
import os

class PunishmentGeneratorService:
    def __init__(self, punishment_doctrine: dict):
        """
        punishment_doctrine = parsed JSON output from PunishmentContextProcessor
        """
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.punishment_doctrine = punishment_doctrine

    def generate_punishment(self, violation: str, severity: str, preferences: list) -> str:
        """
        Create a dynamic punishment based on violation, severity, and user preferences.
        """
        prompt = f"""
You are an AI Punishment Designer.

Given the following punishment philosophy:

Punishment Doctrine:
{self.punishment_doctrine}

Create a NEW, brutal but fitting punishment for the user based on:
- Violation: {violation}
- Severity: {severity}
- User punishment preferences: {', '.join(preferences)}

RULES:
- Match the punishment to the severity.
- Match the punishment category to the user's preferences (if possible).
- Be appropriately harsh for the violation.
- Do NOT just copy examples. Invent something new but true to philosophy.
- Respond ONLY with the punishment description text, no extra commentary.

Begin:
"""

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You generate dynamic punishments for behavioral enforcement."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200,
        )

        punishment = response['choices'][0]['message']['content'].strip()
        return punishment
