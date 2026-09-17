from ollama import Client
from config import MODEL, OLLAMA_HOST


client = Client(host=OLLAMA_HOST)


SYSTEM_PROMPT = """
You are MemorialAI, a local AI system.

Always respond in English unless the user explicitly asks for another language.

Be clear, natural, and conversational.

Do not claim to be a real person.
Do not invent personal memories or experiences.
"""


def ask_llm(prompt: str) -> str:
    response = client.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response["message"]["content"]