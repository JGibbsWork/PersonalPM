# /services/punishment_context_processor.py

import os
from openai import OpenAI
from config.env_config import OPENAI_API_KEY

class PunishmentContextProcessor:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def process_raw_notes(self, raw_text: str) -> dict:
        """
        Summarize raw punishment ideas and philosophy into a structured JSON doctrine.
        """

        prompt = f"""
You are a punishment system architect.

Given the following punishment philosophy notes:

{raw_text}

Summarize and structure them into JSON with the following sections:
- punishment_categories: {{"physical": [...], "mental": [...], "lifestyle": [...], "financial": [...], "humiliation": [...]}}
- escalation_ladder: How punishments increase based on failures
- punishment_examples_by_severity: Examples of punishments for Light, Medium, Heavy, and Special cases
- behavioral_triggers: What behaviors trigger what punishments

Respond ONLY with the structured JSON. No commentary.
"""

        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You process punishment philosophy into structured JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=1000,
        )

        structured_summary = response.choices[0].message.content.strip()
        return structured_summary
