from pathlib import Path
import argparse
import json
import re
from collections import Counter


BASE_DIR = Path(__file__).resolve().parent


SOURCE_DIRS = {
    "prototype": BASE_DIR / "data" / "prototype",
    "person": BASE_DIR / "data" / "person",
}


class ConversationAnalyzer:

    def __init__(self, source="prototype", target_speaker=None):

        if source not in SOURCE_DIRS:
            raise ValueError(
                f"Unknown source '{source}'. "
                f"Available sources: {list(SOURCE_DIRS.keys())}"
            )

        self.source = source
        self.target_speaker = target_speaker

        self.source_dir = SOURCE_DIRS[source]

        self.metadata_file = (
            self.source_dir
            / "metadata"
            / "metadata.json"
        )

    def load_data(self):

        if not self.metadata_file.exists():
            raise FileNotFoundError(
                f"Metadata file not found:\n"
                f"{self.metadata_file}"
            )

        with open(
            self.metadata_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def clean_text(self, text: str) -> str:

        if not text:
            return ""

        text = re.sub(
            r"\[[^\]]+\]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def extract_turns(self, transcript: str):

        pattern = re.compile(
            r"Speaker\s+(\d+)\s+"
            r"\[([0-9:.]+)\s*-\s*([0-9:.]+)\]:\s*"
            r"(.*?)(?=Speaker\s+\d+\s+\[|$)",
            re.DOTALL
        )

        turns = []

        for match in pattern.finditer(transcript or ""):

            speaker = f"Speaker {match.group(1)}"

            start = match.group(2)
            end = match.group(3)

            text = self.clean_text(
                match.group(4)
            )

            if text:

                turns.append({
                    "speaker": speaker,
                    "start": start,
                    "end": end,
                    "text": text,
                })

        return turns

    def detect_language(self, text: str):

        if not text:
            return "unknown"

        devanagari = len(
            re.findall(
                r"[\u0900-\u097F]",
                text
            )
        )

        latin = len(
            re.findall(
                r"[A-Za-z]",
                text
            )
        )

        if devanagari > 0 and latin > 0:
            return "hinglish"

        if devanagari > 0:
            return "hindi"

        if latin > 0:
            return "english"

        return "other"

    def analyze_text(self, turns):

        language_counts = Counter()
        word_counter = Counter()

        total_words = 0
        total_turns = len(turns)

        questions = 0
        short_responses = 0

        for turn in turns:

            text = turn["text"]

            language = self.detect_language(text)

            language_counts[language] += 1

            words = re.findall(
                r"[A-Za-z\u0900-\u097F]+",
                text
            )

            total_words += len(words)

            for word in words:

                word_counter[
                    word.lower()
                ] += 1

            if "?" in text:
                questions += 1

            if len(words) <= 4:
                short_responses += 1

        average_words = (
            total_words / total_turns
            if total_turns
            else 0
        )

        question_rate = (
            questions / total_turns
            if total_turns
            else 0
        )

        short_response_rate = (
            short_responses / total_turns
            if total_turns
            else 0
        )

        return {

            "total_turns": total_turns,

            "total_words": total_words,

            "average_words_per_turn": round(
                average_words,
                2
            ),

            "questions": questions,

            "question_rate": round(
                question_rate,
                3
            ),

            "short_response_rate": round(
                short_response_rate,
                3
            ),

            "language_turns": dict(
                language_counts
            ),

            "common_words":
                word_counter.most_common(20),
        }

    def analyze(self):

        rows = self.load_data()

        all_turns = []

        for row in rows:

            transcript = row.get(
                "transcript",
                ""
            )

            turns = self.extract_turns(
                transcript
            )

            for turn in turns:

                if (
                    self.target_speaker
                    and turn["speaker"]
                    != self.target_speaker
                ):
                    continue

                turn["row_idx"] = row.get(
                    "row_idx"
                )

                all_turns.append(turn)

        return self.analyze_text(
            all_turns
        )


def main():

    parser = argparse.ArgumentParser(
        description="MemorialAI Conversation Style Analyzer"
    )

    parser.add_argument(
        "--source",
        default="prototype",
        choices=[
            "prototype",
            "person"
        ],
        help="Dataset source"
    )

    parser.add_argument(
        "--speaker",
        default=None,
        help="Target speaker, e.g. 'Speaker 2'"
    )

    args = parser.parse_args()

    print("================================")
    print("   MemorialAI Conversation")
    print("        Style Analyzer")
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

    analyzer = ConversationAnalyzer(
        source=args.source,
        target_speaker=args.speaker
    )

    result = analyzer.analyze()

    print("\nTotal turns:")
    print(result["total_turns"])

    print("\nTotal words:")
    print(result["total_words"])

    print("\nAverage words per turn:")
    print(
        result[
            "average_words_per_turn"
        ]
    )

    print("\nQuestions:")
    print(result["questions"])

    print("\nQuestion rate:")
    print(result["question_rate"])

    print("\nShort response rate:")
    print(
        result[
            "short_response_rate"
        ]
    )

    print("\nLanguage distribution:")

    for language, count in result[
        "language_turns"
    ].items():

        print(
            f"  {language}: {count}"
        )

    print("\nCommon words:")

    for word, count in result[
        "common_words"
    ]:

        print(
            f"  {word}: {count}"
        )


if __name__ == "__main__":
    main()