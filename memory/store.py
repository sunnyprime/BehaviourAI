import json
from pathlib import Path
from datetime import datetime


MEMORY_FILE = Path("memory/conversations.json")


def load_memories():
    if not MEMORY_FILE.exists():
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(role: str, content: str):
    memories = load_memories()

    memories.append({
        "timestamp": datetime.now().isoformat(),
        "role": role,
        "content": content
    })

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, ensure_ascii=False, indent=2)