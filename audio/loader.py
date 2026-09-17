from pathlib import Path
import json
import shutil

import requests
from huggingface_hub import hf_hub_download


DATASET_NAME = "liva-ai/hindi-english-asr"

BASE_DIR = Path(__file__).resolve().parent
PROTOTYPE_DIR = BASE_DIR / "data" / "prototype"
AUDIO_DIR = PROTOTYPE_DIR / "audio"
METADATA_DIR = PROTOTYPE_DIR / "metadata"

AUDIO_FILES = [
    "data/A_001_001.mp3",
    "data/A_001_003.mp3",
    "data/A_001_004.mp3",
    "data/A_001_009.mp3",
    "data/A_001_010.mp3",
    "data/A_001_018.mp3",
    "data/A_001_022.mp3",
    "data/A_001_033.mp3",
    "data/A_001_041.mp3",
    "data/A_001_042.mp3",
]


def download_audio():

    AUDIO_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Checking prototype audio...\n")

    for index, repo_file in enumerate(AUDIO_FILES, start=1):

        filename = Path(repo_file).name
        destination = AUDIO_DIR / filename

        if destination.exists():
            print(
                f"[{index}/{len(AUDIO_FILES)}] "
                f"{filename} - already exists"
            )
            continue

        cached_file = hf_hub_download(
            repo_id=DATASET_NAME,
            filename=repo_file,
            repo_type="dataset",
        )

        shutil.copy2(
            cached_file,
            destination,
        )

        print(
            f"[{index}/{len(AUDIO_FILES)}] "
            f"{filename}"
        )


def download_metadata():

    METADATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("\nFetching dataset metadata...")

    url = (
        "https://datasets-server.huggingface.co/rows"
        "?dataset=liva-ai/hindi-english-asr"
        "&config=default"
        "&split=train"
        "&offset=0"
        "&length=100"
    )

    response = requests.get(url, timeout=60)

    response.raise_for_status()

    data = response.json()

    rows = data.get("rows", [])

    print(f"Metadata rows received: {len(rows)}")

    metadata = []

    for row in rows:

        row_data = row.get("row", {})

        item = {
            "row_idx": row.get("row_idx"),
            "duration": row_data.get("duration"),
            "transcript": row_data.get("transcript"),
            "timecodes": row_data.get("timecodes"),
        }

        metadata.append(item)

    output_file = METADATA_DIR / "metadata.json"

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Metadata saved: {output_file}")


def download_prototype_dataset():

    print(f"Dataset: {DATASET_NAME}")

    download_audio()

    download_metadata()

    print("\n================================")
    print("Prototype dataset ready")
    print("================================")

    print(f"Audio: {AUDIO_DIR}")
    print(f"Metadata: {METADATA_DIR}")


if __name__ == "__main__":
    download_prototype_dataset()