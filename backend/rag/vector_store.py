import json
import os
import math
from typing import List, Dict, Any, Tuple

from .embeddings import embed_texts


def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class SimpleVectorStore:
    """
    Lightweight vector store in memory backed by clinic_info.json.
    Good enough for assessment; can be replaced with real DB.
    """

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.docs: List[Dict[str, Any]] = []
        self.embeddings: List[List[float]] = []

    async def load(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.docs = json.load(f)

        texts = [d["content"] for d in self.docs]
        self.embeddings = await embed_texts(texts)

    async def query(self, question: str, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        q_emb = (await embed_texts([question]))[0]
        scored = []
        for doc, emb in zip(self.docs, self.embeddings):
            score = cosine_similarity(q_emb, emb)
            scored.append((doc, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
