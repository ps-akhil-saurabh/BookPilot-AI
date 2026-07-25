"""
BookPilot AI — Embedding Module

Uses sentence-transformers ('all-MiniLM-L6-v2') to generate vector embeddings.
"""

from typing import List
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.core.logger import logger

_model: SentenceTransformer | None = None

def get_embedding_model() -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info(f"Loading SentenceTransformer model: {settings.EMBEDDING_MODEL}")
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate normalized vector embeddings for a list of text strings."""
    if not texts:
        return []
    model = get_embedding_model()
    embeddings = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    return embeddings.tolist()
