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
    Combines subword n-grams and token hash buckets with tf-idf-like weighting.
    """
    clean = re.sub(r"[^\w\s]", " ", text.lower())
    tokens = clean.split()
    if not tokens:
        return [0.0] * dim

    vec = [0.0] * dim

    # Add unigram and bigram frequency hashes
    for i, token in enumerate(tokens):
        # Unigram hash
        h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if (h >> 8) % 2 == 0 else -1.0
        vec[idx] += sign * (1.0 + 1.0 / (len(token) + 1))

        # Bigram hash
        if i < len(tokens) - 1:
            bigram = f"{token}_{tokens[i+1]}"
            hb = int(hashlib.sha256(bigram.encode("utf-8")).hexdigest(), 16)
            b_idx = hb % dim
            b_sign = 1.0 if (hb >> 8) % 2 == 0 else -1.0
            vec[b_idx] += b_sign * 1.5

        # Character trigrams for morphological similarity
        for j in range(len(token) - 2):
            trigram = token[j:j+3]
            ht = int(hashlib.md5(trigram.encode("utf-8")).hexdigest()[:8], 16)
            t_idx = ht % dim
            t_sign = 1.0 if (ht >> 4) % 2 == 0 else -1.0
            vec[t_idx] += t_sign * 0.4

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
            pass  # Fallback to local dense vector

    return compute_deterministic_dense_vector(text)


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two normalized vectors."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    return max(0.0, min(1.0, float(dot)))
