"""
BookPilot AI — Document Chunking Module

Splits raw book text into overlapping semantic chunks for vector embedding and retrieval.
"""

from typing import List, Dict, Any
from app.core.config import settings

class DocumentChunker:
    """Handles text chunking with overlap."""

    def __init__(self, chunk_size: int = settings.CHUNK_SIZE, overlap: int = settings.CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Split raw text into chunks, attaching source metadata."""
        if not text:
            return []

        chunks = []
        start = 0
        text_length = len(text)
        chunk_idx = 0

        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            
            # Adjust end to avoid cutting words in half if possible
            if end < text_length:
                last_space = text.rfind(" ", start, end)
                if last_space != -1 and last_space > start + (self.chunk_size // 2):
                    end = last_space

            chunk_content = text[start:end].strip()

            if chunk_content:
                chunk_meta = metadata.copy()
                chunk_meta["chunk_index"] = chunk_idx
                chunks.append({
                    "id": f"{metadata.get('book_id', 'book')}_{chunk_idx}",
                    "text": chunk_content,
                    "metadata": chunk_meta,
                })
                chunk_idx += 1

            start = end - self.overlap if end < text_length else text_length

        return chunks

chunker = DocumentChunker()
