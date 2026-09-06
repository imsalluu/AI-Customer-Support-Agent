import hashlib
import json
import math
import re
from typing import List
import httpx
from app.core.config import settings

VECTOR_DIM = 384


def _normalize_vector(vec: List[float]) -> List[float]:
    norm = math.sqrt(sum(x * x for x in vec))
    if norm == 0:
        return vec
    return [x / norm for x in vec]


def compute_deterministic_dense_vector(text: str, dim: int = VECTOR_DIM) -> List[float]:
    """
    Generates a dense unit-normalized semantic vector for text.
    Uses positive frequency hashing over unigrams, bigrams, and character trigrams.
    """
    clean = re.sub(r"[^\w\s]", " ", text.lower())
    tokens = [t for t in clean.split() if len(t) > 1]
    if not tokens:
        return [0.0] * dim

    vec = [0.0] * dim

    for i, token in enumerate(tokens):
        # Unigram hash
        h = int(hashlib.md5(token.encode("utf-8")).hexdigest()[:8], 16)
        vec[h % dim] += 1.0 + (1.0 / (len(token) + 1))

        # Bigram hash
        if i < len(tokens) - 1:
            bigram = f"{token}_{tokens[i+1]}"
            hb = int(hashlib.sha256(bigram.encode("utf-8")).hexdigest()[:8], 16)
            vec[hb % dim] += 1.5

        # Character trigrams for morphological root matching
        for j in range(len(token) - 2):
            trigram = token[j:j+3]
            ht = int(hashlib.md5(trigram.encode("utf-8")).hexdigest()[:6], 16)
            vec[ht % dim] += 0.3

    return _normalize_vector(vec)


async def get_embedding(text: str) -> List[float]:
    """Generate vector embedding for text using OpenAI if configured, or deterministic engine."""
    if settings.OPENAI_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(
                    "https://api.openai.com/v1/embeddings",
                    headers={
                        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": settings.EMBEDDING_MODEL,
                        "input": text[:8000],
                    },
                )
                if res.status_code == 200:
                    data = res.json()
                    return data["data"][0]["embedding"]
        except Exception:
            pass

    return compute_deterministic_dense_vector(text)


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two normalized vectors."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    return max(0.0, min(1.0, float(dot)))
