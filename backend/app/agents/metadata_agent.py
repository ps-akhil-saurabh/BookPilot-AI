"""
BookPilot AI — Metadata Agent

Fetches and enriches metadata for books using Browser MCP.
"""

from typing import Dict, Any, List
from app.mcp.browser import browser_mcp
from app.core.logger import get_agent_logger

logger = get_agent_logger("MetadataAgent")

class MetadataAgent:
    """Metadata Agent: Enriches book information."""

    async def process(self, book_titles: List[str]) -> Dict[str, Any]:
        logger.info(f"MetadataAgent: Processing metadata for {len(book_titles)} books")

        results = {}
        for title in book_titles:
            meta = await browser_mcp.get_book_metadata(title)
            results[title] = meta

        return {
            "metadata": results,
            "status": "completed",
        }

metadata_agent = MetadataAgent()
