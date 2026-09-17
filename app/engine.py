from app.llm import ask_llm
from app.prompt_builder import build_prompt


class AIEngine:

    def respond(self, user_input: str) -> str:

        prompt = build_prompt(
            user_input=user_input
        )

        return ask_llm(prompt)