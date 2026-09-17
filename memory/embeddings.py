from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-m3"


class EmbeddingModel:

    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer(MODEL_NAME)
        print("Embedding model loaded.")

    def encode(self, text: str):
        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()


if __name__ == "__main__":
    model = EmbeddingModel()

    text = "Rahul likes cricket and watches matches on weekends."

    embedding = model.encode(text)

    print("\nText:")
    print(text)

    print("\nEmbedding dimensions:")
    print(len(embedding))

    print("\nFirst 10 values:")
    print(embedding[:10])