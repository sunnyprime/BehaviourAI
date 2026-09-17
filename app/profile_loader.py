from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent


class BehaviorProfileLoader:

    def __init__(self, source="prototype"):

        self.profile_file = (
            BASE_DIR
            / "audio"
            / "data"
            / source
            / "metadata"
            / "behavior_profile.json"
        )

    def load(self):

        if not self.profile_file.exists():
            return {}

        with open(
            self.profile_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def format_for_prompt(self):

        profile = self.load()

        if not profile:
            return "No behavior profile available."

        language = profile.get(
            "language_style",
            {}
        )

        response = profile.get(
            "response_style",
            {}
        )

        common_words = profile.get(
            "common_words",
            []
        )

        words = [
            item["word"]
            for item in common_words
        ]

        return f"""
OBSERVED CONVERSATION STYLE

Language distribution:
- Hindi: {language.get("hindi_percent", 0)}%
- English: {language.get("english_percent", 0)}%
- Hinglish: {language.get("hinglish_percent", 0)}%

Response characteristics:
- Average words per turn: {response.get("average_words_per_turn", 0)}
- Question rate: {response.get("question_rate", 0)}
- Short response rate: {response.get("short_response_rate", 0)}

Frequently observed vocabulary:
{", ".join(words)}

IMPORTANT:
- These characteristics are observations from recorded conversations.
- Use them as style guidance, not as facts about the represented person.
- Do not invent memories, experiences, opinions, or personality traits.
- Do not claim to be the real person.
- Do not force the listed words into every response.
""".strip()