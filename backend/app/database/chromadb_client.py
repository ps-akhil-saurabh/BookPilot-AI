"""
BookPilot AI — ChromaDB Client Setup

Initializes ChromaDB for vector storage and semantic search.
Manages collections: books, chapters, notes, highlights.
"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings
from app.core.logger import logger


# ── Client ───────────────────────────────────────────────────────

_client: chromadb.ClientAPI | None = None


def get_chromadb_client() -> chromadb.ClientAPI:
    """Get or create the ChromaDB persistent client."""
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=str(settings.chromadb_path_resolved),
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True,
            ),
        )
        logger.info(f"ChromaDB client initialized at {settings.CHROMADB_PATH}")
    return _client


# ── Collection Names ─────────────────────────────────────────────

BOOKS_COLLECTION = "books_collection"
CHAPTERS_COLLECTION = "chapters_collection"
NOTES_COLLECTION = "notes_collection"
HIGHLIGHTS_COLLECTION = "highlights_collection"


# ── Collection Accessors ─────────────────────────────────────────

def get_books_collection():
    """Get or create the books embedding collection."""
    client = get_chromadb_client()
    return client.get_or_create_collection(
        name=BOOKS_COLLECTION,
        metadata={"description": "Full book embeddings and metadata"},
    )


def get_chapters_collection():
    """Get or create the chapters embedding collection."""
    client = get_chromadb_client()
    return client.get_or_create_collection(
        name=CHAPTERS_COLLECTION,
        metadata={"description": "Chapter-level embeddings for semantic search"},
    )


def get_notes_collection():
    """Get or create the notes embedding collection."""
    client = get_chromadb_client()
    return client.get_or_create_collection(
        name=NOTES_COLLECTION,
        metadata={"description": "User and AI notes embeddings"},
    )


def get_highlights_collection():
    """Get or create the highlights embedding collection."""
    client = get_chromadb_client()
    return client.get_or_create_collection(
        name=HIGHLIGHTS_COLLECTION,
        metadata={"description": "Highlighted passages and important excerpts"},
    )


# ── Initialization ───────────────────────────────────────────────

def init_chromadb():
    """Initialize all ChromaDB collections."""
    get_books_collection()
    get_chapters_collection()
    get_notes_collection()
    get_highlights_collection()
    logger.info("ChromaDB collections initialized")
