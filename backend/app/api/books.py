"""
BookPilot AI — Books API

CRUD endpoints for the book library.
POST/GET/PUT/DELETE /api/v1/books
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database.sqlite import get_db
from app.database.repositories.book_repository import BookRepository
from app.database.repositories.reading_repository import ProgressRepository
from app.schemas.book import BookCreate, BookUpdate, BookResponse, BookListItem
from app.schemas.common import StandardResponse
from app.core.exceptions import BookNotFoundException, DuplicateBookException

router = APIRouter()


@router.post("/books", status_code=201)
async def add_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """Add a new book to the library."""
    repo = BookRepository(db)

    # Check for duplicates
    existing = repo.get_by_title(book_data.title)
    if existing:
        raise DuplicateBookException(book_data.title)

    book = repo.create(book_data.model_dump(exclude_none=True))

    # Initialize progress record
    progress_repo = ProgressRepository(db)
    progress_repo.upsert(book.id, 0, book.total_pages or 0)

    return StandardResponse(
        message="Book added successfully.",
        data={"book_id": book.id, "title": book.title},
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/books", response_model=list[BookListItem])
async def get_all_books(
    search: str = Query(None, description="Search by title or author"),
    genre: str = Query(None, description="Filter by genre"),
    difficulty: str = Query(None, description="Filter by difficulty"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Get all books with optional search and filters."""
    repo = BookRepository(db)
    progress_repo = ProgressRepository(db)

    if search:
        books = repo.search(search, skip=skip, limit=limit)
    elif genre:
        books = repo.get_by_genre(genre)
    elif difficulty:
        books = repo.get_by_difficulty(difficulty)
    else:
        books = repo.get_all(skip=skip, limit=limit)

    # Attach progress to each book
    result = []
    for book in books:
        progress = progress_repo.get_by_book_id(book.id)
        item = BookListItem(
            id=book.id,
            title=book.title,
            author=book.author,
            genre=book.genre,
            total_pages=book.total_pages,
            difficulty=book.difficulty,
            rating=book.rating,
            is_uploaded=bool(book.is_uploaded),
            progress=progress.percentage if progress else 0.0,
        )
        result.append(item)

    return result


@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific book."""
    repo = BookRepository(db)
    book = repo.get_by_id(book_id)

    if not book:
        raise BookNotFoundException(book_id)

    return BookResponse.model_validate(book)


@router.put("/books/{book_id}")
async def update_book(
    book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)
):
    """Update book information."""
    repo = BookRepository(db)

    book = repo.update(book_id, book_data.model_dump(exclude_none=True))
    if not book:
        raise BookNotFoundException(book_id)

    return StandardResponse(
        message="Book updated successfully.",
        data={"book_id": book.id},
        timestamp=datetime.now(timezone.utc),
    )


@router.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book and all associated data (cascading)."""
    repo = BookRepository(db)

    if not repo.get_by_id(book_id):
        raise BookNotFoundException(book_id)

    repo.delete(book_id)

    return StandardResponse(
        message="Book deleted successfully.",
        data={"book_id": book_id},
        timestamp=datetime.now(timezone.utc),
    )
