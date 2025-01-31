# app/services/openai_service.py
import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_ai_response(user_input):
    """Generate a conversational AI response."""
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant helping with daily tasks."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content
