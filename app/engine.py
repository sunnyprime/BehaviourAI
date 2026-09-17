from app.llm import ask_llm
from app.prompt_builder import build_prompt
from app.behavior import BehaviorEngine


class AIEngine:

    def __init__(self):
        self.behavior = BehaviorEngine()

    def respond(self, user_input: str) -> str:

        behavior_profile = self.behavior.get_profile()

        prompt = build_prompt(
            user_input=user_input,
            behavior_profile=behavior_profile
        )

        return ask_llm(prompt)