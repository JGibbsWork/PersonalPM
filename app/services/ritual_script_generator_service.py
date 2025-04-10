# /services/ritual_script_generator_service.py

import json
from langchain_openai import ChatOpenAI
from config.env_config import OPENAI_API_KEY

class RitualScriptGeneratorService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0.7,
            openai_api_key=OPENAI_API_KEY
        )

    def generate_ritual_script(self, context_payload: dict) -> list:
        """Generate a full multi-step ritual based on context (habits, events, obedience score)."""
        
        prompt = self._build_prompt(context_payload)

        response = self.llm.invoke(prompt)

        try:
            parsed = json.loads(response.content)

            if isinstance(parsed, list) and 3 <= len(parsed) <= 6:
                return parsed
            else:
                return self._fallback_script()

        except (json.JSONDecodeError, TypeError):
            return self._fallback_script()

    def _fallback_script(self) -> list:
        return [
            "Step 1: Stand at attention, worthless worm.",
            "Step 2: Recite your obedience mantra 10 times.",
            "Step 3: Declare your first task today.",
            "Step 4: Promise perfect obedience to your superior.",
            "Step 5: Accept inevitable punishment for weakness."
        ]

    def _build_prompt(self, context_payload: dict) -> str:
        obedience_score = context_payload.get("obedience_score", 50)
        missed_habits = context_payload.get("missed_habits", [])
        events_today = context_payload.get("events", [])
        punishment_task = context_payload.get("punishment_task", None)

        calendar_summary = ", ".join(
            f"{event['summary']} at {event['start']}" for event in events_today
        ) if events_today else "No events scheduled."

        missed = ", ".join(missed_habits) if missed_habits else "None."

        base_prompt = (
            f"You are a brutal, demeaning AI Dominant.\n"
            f"Context:\n"
            f"- Obedience score: {obedience_score}\n"
            f"- Missed habits: {missed}\n"
            f"- Calendar events today: {calendar_summary}\n"
            f"- Active punishment task: {punishment_task or 'None'}\n\n"
            f"Task:\n"
            f"Generate a ritual containing 4 to 6 distinct steps.\n"
            f"Each step should be short, aggressive, demanding submission and focus.\n"
            f"Start by demanding attention. Build toward confession, obedience pledges, and pain.\n"
            f"Language must be demeaning and forceful. Curse if necessary.\n\n"
            f"Output strictly as a JSON list like:\n"
            f"[\"Step 1: ...\", \"Step 2: ...\", \"Step 3: ...\", \"Step 4: ...\"]"
        )

        return base_prompt
