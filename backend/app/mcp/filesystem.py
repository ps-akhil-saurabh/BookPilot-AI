"""
BookPilot AI — Filesystem MCP Tool Integration

Accesses local uploaded files (PDF, EPUB, MD) for text extraction and document inspection.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from app.core.logger import get_mcp_logger
from app.core.exceptions import FileUploadException

logger = get_mcp_logger("FilesystemMCP")

class FilesystemMCP:
    """Filesystem MCP tool for uploaded content access."""

    def read_file_content(self, file_path: str) -> Dict[str, Any]:
        """Extract text from local files (PDF, EPUB, Markdown)."""
        path = Path(file_path)
        if not path.exists():
            raise FileUploadException(f"File not found at path: {file_path}")

        ext = path.suffix.lower()
        logger.info(f"FilesystemMCP: Reading content from {path.name} ({ext})")

        if ext == ".pdf":
            return self._extract_pdf(path)
        elif ext == ".epub":
            return self._extract_epub(path)
        elif ext in [".md", ".txt"]:
            return self._extract_text(path)
        else:
            raise FileUploadException(f"Unsupported extension: {ext}")

    def _extract_pdf(self, path: Path) -> Dict[str, Any]:
        import fitz  # PyMuPDF
        doc = fitz.open(path)
        pages_text = []
        for i, page in enumerate(doc):
            pages_text.append({"page_number": i + 1, "text": page.get_text()})
        
        full_text = "\n\n".join([p["text"] for p in pages_text])
        return {
            "filename": path.name,
            "total_pages": len(doc),
            "text": full_text,
            "pages": pages_text,
        }

    def _extract_epub(self, path: Path) -> Dict[str, Any]:
        import ebooklib
        from ebooklib import epub
        from bs4 import BeautifulSoup

        book = epub.read_epub(path)
        chapters = []
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text = soup.get_text()
            if text.strip():
                chapters.append(text.strip())

        full_text = "\n\n".join(chapters)
        return {
            "filename": path.name,
            "total_pages": len(chapters),  # Chapters as proxy pages
            "text": full_text,
            "pages": [{"page_number": i + 1, "text": c} for i, c in enumerate(chapters)],
        }

    def _extract_text(self, path: Path) -> Dict[str, Any]:
        text = path.read_text(encoding="utf-8")
        return {
            "filename": path.name,
            "total_pages": max(1, len(text) // 2000),
            "text": text,
            "pages": [{"page_number": 1, "text": text}],
        }

filesystem_mcp = FilesystemMCP()
