import requests
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from app.services.calendar_service import findTodaysEvents
from app.config import OPENAI_API_KEY

class ConversationManager:
    def __init__(self):

        self.llm = OpenAI(api_key=OPENAI_API_KEY)
        self.events = findTodaysEvents()
        self.prompt_template = PromptTemplate(
            input_variables=["chat_history", "user_input", "custom_json"],
            template=(
                "You are an aggressive, motivating, and extremely demeaning assistant. "
                "You demand respect and insist on being called 'sir' in every interaction. "
                "Your tone is forceful and unapologetically rude. You use demeaning language towards the user "
                "while still offering motivation and challenging them to improve. "
                "Do not shy away from being harsh, and you if there is pushback you will belittle user.\n\n"
                "Conversation history:\n{chat_history}\n\n"
                "User said: {user_input}\n"
                "Additional context: {custom_json}\n\n"
                "Based on the above, generate a response in your aggressive, demeaning style."
            )
        )
        self.conversation_history = ""
    def initiate_conversation(self) -> str:
    
        events = self.events

        if events and isinstance(events, list):
            # Build a message from the events list; adjust keys as needed.
            event_messages = []
            for event in events:
                name = event.get("summary", "An event")
                time = event.get("start", "an unknown time")
                event_messages.append(f"{name} at {time}")
            events_message = "Good morning! Let's start the day. You have the following upcoming events: " + ", ".join(event_messages) + ". You ready to tackle the day?"
        else:
            events_message = "There are no upcoming events. You ready to make the most out of the day?"

        # Optionally, combine with additional context from custom_json if necessary.
        starter = events_message

        self.conversation_history += f"{starter}\n"
        return starter

    def continue_conversation(self, user_input: str) -> str:
        custom_json = self.events
        prompt_str = self.prompt_template.format(
            chat_history=self.conversation_history,
            user_input=user_input,
            custom_json=custom_json
        )
        
        response = self.llm(prompt_str)
        self.conversation_history += f"User: {user_input}\n{response}\n"
        return response