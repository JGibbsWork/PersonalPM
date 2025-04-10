# /services/sentiment_service.py

import openai
import os

class SentimentService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def analyze_behavioral_sentiment(self, text: str) -> str:
        """
        Analyze user behavior for obedience, respect, and submission levels.

        Returns one of:
        - Highly Submissive
        - Submissive
        - Neutral
        - Disrespectful
        - Disobedient
        - Aggressively Disobedient
        """
        prompt = f"""
You are a behavioral classifier trained to detect obedience, respect, and submission.

Classify the following message as exactly one of:
- Highly Submissive
- Submissive
- Neutral
- Disrespectful
- Disobedient
- Aggressively Disobedient

Definitions:
- Highly Submissive: Fully respectful, worshipful, eager to please.
- Submissive: Polite, respectful, obedient.
- Neutral: No particular attitude, basic cooperation.
- Disrespectful: Mild rudeness, sarcasm, passive-aggressiveness.
- Disobedient: Resistance, refusal to obey, argumentative tone.
- Aggressively Disobedient: Open rebellion, insult, hostility, aggressive defiance.

Message:
{text}

Respond ONLY with the exact label listed above.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You classify user messages into behavioral obedience categories."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=10,
        )

        classification = response['choices'][0]['message']['content'].strip()
        return classification

    def detect_apology(self, text: str) -> bool:
        """
        Detect if user is genuinely apologizing.

        Simple keyword check for now. (Later could upgrade to full LLM analysis.)
        """
        apology_keywords = [
            "i'm sorry", "i apologize", "please forgive me", "sorry", "forgive me",
            "i regret", "i beg forgiveness"
        ]

        text_lower = text.lower()

        return any(phrase in text_lower for phrase in apology_keywords)
