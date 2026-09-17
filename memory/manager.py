from memory.database import save_message, get_messages


class MemoryManager:

    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id

    def save_user_message(self, text: str):
        save_message(
            self.conversation_id,
            "user",
            text
        )

    def save_ai_message(self, text: str):
        save_message(
            self.conversation_id,
            "assistant",
            text
        )

    def get_conversation(self):
        return get_messages(self.conversation_id)

    def get_context(self) -> str:
        messages = self.get_conversation()

        if not messages:
            return ""

        return "\n".join(
            f"{speaker}: {text}"
            for _, _, speaker, text, _ in messages
        )