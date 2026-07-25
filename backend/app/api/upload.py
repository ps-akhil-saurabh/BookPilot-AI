"""
BookPilot AI — File Upload API

Endpoints for uploading PDFs, EPUBs, and Markdown files for RAG processing.
"""

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database.sqlite import get_db
from app.database.repositories.book_repository import BookRepository
from app.core.security import validate_file_type, validate_file_size, sanitize_filename
from app.core.config import settings
from app.mcp.filesystem import filesystem_mcp
from app.rag.chunking import chunker
from app.rag.indexing import index_book_chunks
from app.schemas.common import StandardResponse

router = APIRouter()

@router.post("/upload/book", status_code=201)
async def upload_book(
    file: UploadFile = File(...),
    title: str = Form(None),
    author: str = Form(None),
    db: Session = Depends(get_db),
):
    """Upload a book file (PDF, EPUB, MD), extract text, and index into ChromaDB."""
    ext = validate_file_type(file.filename)
    safe_name = sanitize_filename(file.filename)

    file_bytes = await file.read()
    validate_file_size(len(file_bytes))

    # Save file to upload directory
    save_path = settings.upload_path / safe_name
    save_path.write_bytes(file_bytes)

    # Extract text using Filesystem MCP
    extracted = filesystem_mcp.read_file_content(str(save_path))
    text_content = extracted["text"]
    total_pages = extracted["total_pages"]
    book_title = title or extracted["filename"].rsplit(".", 1)[0]

    # Save to SQLite
    book_repo = BookRepository(db)
    book = book_repo.create({
        "title": book_title,
        "author": author or "Unknown",
        "total_pages": total_pages,
        "file_path": str(save_path),
        "is_uploaded": 1,
    })

    # Chunk and index into ChromaDB
    chunks = chunker.chunk_text(text_content, {"book_id": book.id, "title": book.title})
    index_book_chunks(book.id, book.title, chunks)

    return StandardResponse(
        message="Book uploaded and indexed successfully.",
        data={
            "book_id": book.id,
            "title": book.title,
            "total_pages": total_pages,
            "indexed_chunks": len(chunks),
        },
        timestamp=datetime.now(timezone.utc),
    )
