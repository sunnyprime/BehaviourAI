import uuid

from app.llm import ask_llm
from app.prompt_builder import build_prompt
from memory.manager import MemoryManager


class AIEngine:

    def __init__(self):
        self.conversation_id = str(uuid.uuid4())
        self.memory = MemoryManager(self.conversation_id)

    def respond(self, user_input: str) -> str:

        self.memory.save_user_message(user_input)

        conversation_context = self.memory.get_context()

        prompt = build_prompt(
            user_input=user_input,
            memories=conversation_context
        )

        response = ask_llm(prompt)

        self.memory.save_ai_message(response)

        return response