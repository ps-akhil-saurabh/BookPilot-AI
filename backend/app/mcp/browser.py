"""
BookPilot AI — Browser MCP Tool Integration

Provides metadata retrieval for books via online sources (Open Library API / Google Books fallback).
"""

import httpx
from typing import Dict, Any, Optional
from app.core.logger import get_mcp_logger
from app.core.constants import Difficulty

logger = get_mcp_logger("BrowserMCP")

class BrowserMCP:
    """Browser MCP tool for external book metadata retrieval."""

    def __init__(self):
        self.open_library_url = "https://openlibrary.org/search.json"
        self.google_books_url = "https://www.googleapis.com/books/v1/volumes"

    async def get_book_metadata(self, title: str, author: Optional[str] = None) -> Dict[str, Any]:
        """Fetch book metadata including page count, genre, ratings, author, and estimated difficulty."""
        logger.info(f"BrowserMCP: Fetching metadata for '{title}' (Author: {author})")

        # Try Open Library API first
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                params = {"title": title}
                if author:
                    params["author"] = author
                
                res = await client.get(self.open_library_url, params=params)
                if res.status_code == 200:
                    data = res.json()
                    docs = data.get("docs", [])
                    if docs:
                        doc = docs[0]
                        num_pages = doc.get("number_of_pages_median") or doc.get("number_of_pages") or 250
                        genres = doc.get("subject", [])
                        genre = genres[0] if genres else "General"
                        author_name = doc.get("author_name", [author or "Unknown"])[0]
                        rating = doc.get("ratings_average", 4.2)
                        
                        difficulty = self._estimate_difficulty(num_pages, genres)

                        logger.info(f"BrowserMCP: Retrieved metadata from Open Library for '{title}'")
                        return {
                            "title": doc.get("title", title),
                            "author": author_name,
                            "pages": num_pages,
                            "genre": genre,
                            "rating": round(float(rating), 2),
                            "difficulty": difficulty,
                            "source": "Open Library",
                        }
        except Exception as e:
            logger.warning(f"BrowserMCP: Open Library request failed: {e}")

        # Fallback metadata generator if external API fails or yields nothing
        logger.info(f"BrowserMCP: Using heuristic fallback metadata for '{title}'")
        return {
            "title": title,
            "author": author or "Unknown Author",
            "pages": 300,
            "genre": "General Non-Fiction",
            "rating": 4.5,
            "difficulty": Difficulty.MEDIUM,
            "source": "Heuristic Fallback",
        }

    def _estimate_difficulty(self, pages: int, genres: list) -> str:
        genre_str = " ".join([g.lower() for g in genres[:5]]) if genres else ""
        if any(term in genre_str for term in ["quantum", "philosophy", "neuroscience", "math", "algorithms", "physics", "deep learning"]):
            return Difficulty.HARD
        elif pages > 500:
            return Difficulty.HARD
        elif pages < 200:
            return Difficulty.EASY
        return Difficulty.MEDIUM

browser_mcp = BrowserMCP()
