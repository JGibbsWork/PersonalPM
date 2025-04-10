# /services/sentiment_service.py

import openai
import os

class SentimentService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def analyze_sentiment(self, text: str):
        """Analyze text sentiment."""
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Classify the sentiment of the following text as Positive, Neutral, or Negative:\n\n{text}\n\nSentiment:",
            max_tokens=1
        )
        sentiment = response.choices[0].text.strip()
        return sentiment
