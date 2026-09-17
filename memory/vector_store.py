from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from memory.embeddings import EmbeddingModel


QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "memorial_memories"
VECTOR_SIZE = 1024


class VectorStore:

    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL)
        self.embedding_model = EmbeddingModel()

    def create_collection(self):

        if self.client.collection_exists(COLLECTION_NAME):
            return

        self.client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

    def add_memory(
        self,
        memory_id: str,
        text: str,
        category: str,
        confidence: float,
        source: str,
    ):

        embedding = self.embedding_model.encode(text)

        point = PointStruct(
            id=memory_id,
            vector=embedding,
            payload={
                "text": text,
                "category": category,
                "confidence": confidence,
                "source": source,
            },
        )

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point],
        )

        print(f"Memory stored: {memory_id}")

    def search(self, query: str, limit: int = 3):

        query_embedding = self.embedding_model.encode(query)

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=limit,
        ).points

        return results