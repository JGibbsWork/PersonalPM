import re
import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from utils.prompt_loader import load_prompt
from config.env_config import OPENAI_API_KEY

api_key=OPENAI_API_KEY

class MantraService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0.7,
            openai_api_key=api_key
        )
        self.system_prompt = load_prompt("prompts/dom.txt")
        self.system_prompt = """[PASTE YOUR FULL DOMINANT OVERSEER PROMPT HERE]"""

    def generate_mantra(self):
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content="Begin the morning call. Invent today's obedience mantra and instruct the servant to repeat it."),
        ]

        response = self.llm(messages)
        generated_text = response.content

        mantra, repetitions = self._parse_response(generated_text)
        return mantra, repetitions

    def _parse_response(self, text):
        # Basic regex extraction
        mantra_match = re.search(r'["“](.*?)["”]', text)
        repetitions_match = re.search(r'(\d+)\s*(?:times|repetitions)', text)

        mantra = mantra_match.group(1) if mantra_match else "Obey without hesitation."
        repetitions = int(repetitions_match.group(1)) if repetitions_match else 3

        return mantra, repetitions
