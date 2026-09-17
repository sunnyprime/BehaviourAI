import uuid

from memory.extractor import MemoryExtractor
from memory.vector_store import VectorStore


class MemoryService:

    def __init__(self):
        self.extractor = MemoryExtractor()
        self.vector_store = VectorStore()

        self.vector_store.create_collection()

    def process_message(self, text: str, source: str = "chat"):

        result = self.extractor.extract(text)

        if not result.get("is_memory"):
            return None

        memory_id = str(uuid.uuid4())

        memory = result["memory"]
        category = result["category"]
        confidence = result["confidence"]

        self.vector_store.add_memory(
            memory_id=memory_id,
            text=memory,
            category=category,
            confidence=confidence,
            source=source,
        )

        return {
            "id": memory_id,
            "memory": memory,
            "category": category,
            "confidence": confidence,
        }