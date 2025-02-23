import requests
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from app.services.calendar_service import findTodaysEvents


class ConversationManager:
    def __init__(self, api_key: str):
        # Initialize your LLM (OpenAI API is used here)
        self.llm = OpenAI(api_key=api_key)
        self.prompt_template = PromptTemplate(
            input_variables=["chat_history", "user_input", "custom_json"],
            template=(
                "Conversation history:\n{chat_history}\n\n"
                "User said: {user_input}\n"
                "Additional context: {custom_json}\n\n"
                "Based on the above, generate a conversational and context-aware response."
            )
        )
        self.conversation_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        # This example uses a simple string for conversation history.
        # In production, manage state per user (e.g., using the caller's phone number).
        self.conversation_history = ""

    def fetch_custom_json(self):
        """Fetch custom JSON data from your external API."""
        try:
            response = findTodaysEvents()
            return response.json()
        except Exception:
            return {"error": "Failed to retrieve custom JSON"}

    def initiate_conversation(self) -> str:
        """
        For the first interaction, use the custom JSON to determine a dynamic starter message.
        Expects the JSON to contain a key 'starter'.
        """
        custom_json = self.fetch_custom_json()
        starter = custom_json.get("starter", "Hello, how can I help you today?")
        self.conversation_history += f"AI: {starter}\n"
        return starter

    def continue_conversation(self, user_input: str) -> str:
        """
        Generate a context-aware response using the entire conversation history,
        the latest user input, and current custom JSON context.
        """
        custom_json = self.fetch_custom_json()
        response = self.conversation_chain.run(
            chat_history=self.conversation_history,
            user_input=user_input,
            custom_json=custom_json
        )
        self.conversation_history += f"User: {user_input}\nAI: {response}\n"
        return response
