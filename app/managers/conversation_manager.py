# /managers/conversation_manager.py

import requests
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from config.env_config import OPENAI_API_KEY
from utils.prompt_loader import load_prompt
from services.sentiment_service import SentimentService
from services.obedience_service import ObedienceService

sentiment_service = SentimentService()
obedience_service = ObedienceService()

api_key = OPENAI_API_KEY

class ConversationManager:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0.7,
            openai_api_key=api_key
        )
        self.system_prompt = load_prompt("prompts/dom.txt")
        self.prompt_template = PromptTemplate(
            input_variables=["chat_history", "user_input", "custom_json"],
            template=(
                "You are an aggressive, motivating, and extremely demeaning assistant who freely uses explicit language. "
                "Do not hold back—be blunt, direct, and let the language flow naturally.\n\n"
                "Conversation history:\n{chat_history}\n\n"
                "User said: {user_input}\n"
                "Additional context: {custom_json}\n\n"
                "Based on the above, generate a response in your aggressive, demeaning style."
            )
        )
        self.conversation_history = ""

    def initiate_conversation(self, context_payload: dict) -> str:
        """Start a conversation based on provided context."""
        prompt_str = self.prompt_template.format(
            chat_history=self.conversation_history,
            user_input="(system initiated)",
            custom_json=context_payload
        )

        response = self.llm(prompt_str)
        self.conversation_history += f"System: {response}\n"
        return response

    def continue_conversation(self, user_input: str, context_payload: dict = None) -> str:
        """Continue the conversation based on user input (with optional updated context)."""
        if context_payload is None:
            context_payload = {}

        prompt_str = self.prompt_template.format(
            chat_history=self.conversation_history,
            user_input=user_input,
            custom_json=context_payload
        )
        # After generating prompt_str but before LLM call

        classification = sentiment_service.analyze_behavioral_sentiment(user_input)

        if sentiment_service.detect_apology(user_input):
            print("🕊 Forgiveness detected. Offering mercy...")
            obedience_service.offer_forgiveness()
        else:
            if classification in ["Highly Submissive", "Submissive"]:
                obedience_service.reward_for_respect()
            elif classification == "Neutral":
                pass  # No change
            elif classification == "Disrespectful":
                obedience_service.penalize_minor_disrespect()
            elif classification == "Disobedient":
                obedience_service.penalize_major_disobedience()
            elif classification == "Aggressively Disobedient":
                obedience_service.penalize_severe_disobedience()


        response = self.llm(prompt_str)
        self.conversation_history += f"User: {user_input}\n{response}\n"
        return response
