from pathlib import Path
import json
import argparse

from audio.analyzer import ConversationAnalyzer


BASE_DIR = Path(__file__).resolve().parent


class BehaviorProfileBuilder:

    def __init__(self, source="prototype", speaker=None):

        self.source = source
        self.speaker = speaker

        self.analyzer = ConversationAnalyzer(
            source=source,
            target_speaker=speaker,
        )

    def build(self):

        result = self.analyzer.analyze()

        language_turns = result["language_turns"]

        total_turns = result["total_turns"]

        hindi = language_turns.get("hindi", 0)
        english = language_turns.get("english", 0)
        hinglish = language_turns.get("hinglish", 0)

        if total_turns:

            hindi_percent = round(
                hindi / total_turns * 100,
                1
            )

            english_percent = round(
                english / total_turns * 100,
                1
            )

            hinglish_percent = round(
                hinglish / total_turns * 100,
                1
            )

        else:

            hindi_percent = 0
            english_percent = 0
            hinglish_percent = 0

        profile = {

            "source": self.source,

            "target_speaker": self.speaker,

            "sample_size": {
                "turns": total_turns,
                "words": result["total_words"],
            },

            "language_style": {

                "hindi_turns": hindi,

                "english_turns": english,

                "hinglish_turns": hinglish,

                "hindi_percent": hindi_percent,

                "english_percent": english_percent,

                "hinglish_percent": hinglish_percent,
            },

            "response_style": {

                "average_words_per_turn":
                    result[
                        "average_words_per_turn"
                    ],

                "question_rate":
                    result["question_rate"],

                "short_response_rate":
                    result[
                        "short_response_rate"
                    ],
            },

            "common_words": [
                {
                    "word": word,
                    "count": count,
                }
                for word, count
                in result["common_words"]
            ],
        }

        return profile

    def save(self, profile):

        output_dir = (
            BASE_DIR
            / "data"
            / self.source
            / "metadata"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
            output_dir
            / "behavior_profile.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                profile,
                file,
                ensure_ascii=False,
                indent=2
            )

        return output_file


def main():

    parser = argparse.ArgumentParser(
        description="Build MemorialAI behavior profile"
    )

    parser.add_argument(
        "--source",
        default="prototype",
        choices=[
            "prototype",
            "person",
        ],
    )

    parser.add_argument(
        "--speaker",
        default=None,
    )

    args = parser.parse_args()

    print("================================")
    print("    MemorialAI Behavior Profile")
    print("================================")

    print(f"\nSource: {args.source}")

    if args.speaker:
        print(
            f"Target speaker: {args.speaker}"
        )
    else:
        print(
            "Target speaker: ALL SPEAKERS"
        )

    builder = BehaviorProfileBuilder(
        source=args.source,
        speaker=args.speaker,
    )

    profile = builder.build()

    output_file = builder.save(
        profile
    )

    print("\nProfile created successfully.")

    print(
        f"\nSaved to:\n{output_file}"
    )

    print("\nProfile:")

    print(
        json.dumps(
            profile,
            ensure_ascii=False,
            indent=2
        )
    )


if __name__ == "__main__":
    main()