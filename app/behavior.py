class BehaviorEngine:

    def __init__(self):
        self.profile = {}

    def get_profile(self) -> str:
        if not self.profile:
            return "No behavior profile available yet."

        return str(self.profile)