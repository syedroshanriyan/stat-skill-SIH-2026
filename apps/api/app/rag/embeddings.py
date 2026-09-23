import math
import hashlib
from typing import List
from app.core.config import settings


def generate_embedding(text: str, dimensions: int = 768) -> List[float]:
    # If Gemini API Key is configured, attempt live Gemini text-embedding
    if settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY) > 10:
        try:
            from google import genai
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            result = client.models.embed_content(
                model="text-embedding-004",
                contents=text
            )
            if hasattr(result, "embedding") and hasattr(result.embedding, "values"):
                return list(result.embedding.values)
        except Exception:
            pass  # Fallback to deterministic normalized embedding

    # Deterministic semantic projection for offline/test environments
    # Generates a reproducible unit-normalized vector from text tokens
    vec = [0.0] * dimensions
    words = text.lower().split()
    if not words:
        words = ["empty"]

    for w in words:
        h = int(hashlib.sha256(w.encode("utf-8")).hexdigest()[:8], 16)
        idx = h % dimensions
        sign = 1.0 if (h % 2 == 0) else -1.0
        vec[idx] += sign

    # Unit normalize
    magnitude = math.sqrt(sum(x * x for x in vec))
    if magnitude > 0:
        vec = [round(x / magnitude, 5) for x in vec]
    return vec


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0
    dot = sum(a * b for a, b in zip(vec1, vec2))
    return max(0.0, min(1.0, dot))
