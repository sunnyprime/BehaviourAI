from app.llm import ask_llm
from app.prompt_builder import build_prompt
from memory.database import save_message, get_messages
import uuid


class AIEngine:

    def __init__(self):
        self.conversation_id = str(uuid.uuid4())

    def respond(self, user_input: str) -> str:

        # Save user message
        save_message(
            self.conversation_id,
            "user",
            user_input
        )

        # Get previous conversation
        messages = get_messages(self.conversation_id)

        conversation_history = "\n".join(
            f"{speaker}: {text}"
            for _, _, speaker, text, _ in messages
        )

        prompt = build_prompt(
            user_input=user_input,
            memories=conversation_history
        )

        response = ask_llm(prompt)

        # Save AI response
        save_message(
            self.conversation_id,
            "assistant",
            response
        )

        return response