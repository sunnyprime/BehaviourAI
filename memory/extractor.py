import json

from app.llm import ask_llm


class MemoryExtractor:

    def extract(self, text: str):

        prompt = f"""
You are a memory extraction system for MemorialAI.

Analyze the user's message and determine whether it contains
a useful long-term personal memory.

Only extract information that is explicitly stated.

Do NOT infer:
- personality
- emotions
- relationships
- beliefs
- intentions
- facts that are not directly stated

Do NOT extract temporary conversation such as:
- greetings
- questions
- requests
- casual small talk
- temporary plans
- current weather
- one-time instructions

Potential memory categories:
- identity
- family
- relationships
- preferences
- life_event
- experience
- habit
- belief
- communication_style
- fact

Return ONLY valid JSON in this exact format:

{{
    "is_memory": true,
    "category": "preference",
    "memory": "Rahul likes cricket",
    "confidence": 0.95
}}

If the message does not contain useful long-term memory:

{{
    "is_memory": false,
    "category": null,
    "memory": null,
    "confidence": 0.0
}}

USER MESSAGE:
{text}
"""

        response = ask_llm(prompt)

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            return {
                "is_memory": False,
                "category": None,
                "memory": None,
                "confidence": 0.0,
            }


if __name__ == "__main__":

    extractor = MemoryExtractor()

    tests = [
        "My name is Rahul.",
        "I love cricket.",
        "What is the weather today?",
        "My father taught me cricket when I was eight.",
        "Can you explain React hooks?",
    ]

    for text in tests:

        print("\nUSER:", text)

        result = extractor.extract(text)

        print("RESULT:", result)