"""
BookPilot AI — Semantic Retrieval Module

Queries ChromaDB collections to fetch top-K relevant chunks for RAG.
"""

from typing import List, Dict, Any
from app.database.chromadb_client import get_books_collection
from app.rag.embedding import generate_embeddings
from app.core.config import settings
from app.core.logger import logger

def retrieve_relevant_chunks(
    query: str,
    book_id: int | None = None,
    top_k: int = settings.TOP_K_RESULTS
) -> List[Dict[str, Any]]:
    """Retrieve semantically similar text chunks from ChromaDB."""
    collection = get_books_collection()
    
    query_embedding = generate_embeddings([query])[0]
    
    where_filter = {}
    if book_id is not None:
        where_filter["book_id"] = book_id

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_filter if where_filter else None,
    )

    retrieved_chunks = []
    if results and "documents" in results and results["documents"]:
        documents = results["documents"][0]
        metadatas = results["metadatas"][0] if "metadatas" in results else [{}] * len(documents)
        distances = results["distances"][0] if "distances" in results else [0.0] * len(documents)

        for doc, meta, dist in zip(documents, metadatas, distances):
            retrieved_chunks.append({
                "text": doc,
                "metadata": meta,
                "distance": round(dist, 4),
            })

    logger.info(f"RAG Retrieval: Found {len(retrieved_chunks)} relevant chunks for query: '{query}'")
    return retrieved_chunks
