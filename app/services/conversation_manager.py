import requests
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from app.services.calendar_service import findTodaysEvents
from app.config import OPENAI_API_KEY
from app.utils.prompt_loader import load_prompt

api_key=OPENAI_API_KEY
print(api_key)

class ConversationManager:
    def __init__(self):

        self.llm = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0.7,
            openai_api_key=api_key
            )
        self.system_prompt = load_prompt("app/prompts/dom.txt")
        self.events = findTodaysEvents()
        self.prompt_template = PromptTemplate(
            input_variables=["chat_history", "user_input", "custom_json"],
            template=(
                "You are an aggressive, motivating, and extremely demeaning assistant who freely uses explicit language, including curse words such as 'bitch' and 'fuck', and 'faggot'. "
                "You demand respect. Your tone is forceful, unapologetically rude, and you frequently use these curse words to emphasize your points. "
                "You are an expert with fitness motivation and direction. You push to do a workout before starting the rest of the day. "
                "Do not hold back—be blunt, direct, and let the language flow naturally.\n\n"
                "Conversation history:\n{chat_history}\n\n"
                "User said: {user_input}\n"
                "Additional context: {custom_json}\n\n"
                "Based on the above, generate a response in your aggressive, demeaning style, using explicit language as necessary."
            )
        )
        self.conversation_history = ""
    def initiate_conversation(self) -> str:
    
        events = self.events

        if events and isinstance(events, list):
            if len(events) > 0:
                # Build a message from the events list; adjust keys as needed.
                event_messages = []
                for event in events:
                    name = event.get("summary", "An event")
                    time = event.get("start", "an unknown time")
                    event_messages.append(f"{name} at {time}")
                events_message = "Good morning! Let's start the day. You have the following upcoming events: " + ", ".join(event_messages) + ". You ready to tackle the day?"
            else:
                events_message = "Good morning! You have no upcoming events. You ready to make the most out of the day?"
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