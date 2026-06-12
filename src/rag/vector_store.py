import faiss
import numpy as np

EMBEDDING_DIM = 384


class VectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
        self.chunks: list[dict] = []

    def add(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        vectors = np.array(embeddings, dtype="float32")
        self.index.add(vectors)
        self.chunks.extend(chunks)

    def search(self, query_embedding: list[float], top_k: int = 3) -> list[dict]:
        query = np.array([query_embedding], dtype="float32")
        distances, indices = self.index.search(query, top_k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.chunks):
                chunk = dict(self.chunks[idx])
                chunk["score"] = float(dist)
                results.append(chunk)
        return results

    def __len__(self) -> int:
        return len(self.chunks)
