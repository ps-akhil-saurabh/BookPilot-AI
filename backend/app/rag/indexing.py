"""
BookPilot AI — Indexing Module

Indexes chunked documents into ChromaDB collections.
"""

from typing import List, Dict, Any
from app.database.chromadb_client import get_books_collection, get_chapters_collection
from app.rag.embedding import generate_embeddings
from app.core.logger import logger

def index_book_chunks(book_id: int, title: str, chunks: List[Dict[str, Any]]):
    """Index chunks into ChromaDB."""
    if not chunks:
        logger.warning(f"No chunks to index for book ID {book_id}")
        return

    collection = get_books_collection()

    ids = [f"book_{book_id}_chunk_{c['metadata']['chunk_index']}" for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    embeddings = generate_embeddings(documents)

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    logger.info(f"Indexed {len(chunks)} chunks in ChromaDB for book '{title}' (ID {book_id})")
