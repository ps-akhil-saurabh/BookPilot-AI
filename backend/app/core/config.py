"""
BookPilot AI — Application Configuration

Centralized settings management using Pydantic BaseSettings.
All values are configurable via environment variables or .env file.
"""

from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ── Application ──────────────────────────────────────────────
    APP_NAME: str = "BookPilot AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    # ── Server ───────────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ── Database ─────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./bookpilot.db"

    # ── ChromaDB ─────────────────────────────────────────────────
    CHROMADB_PATH: str = "./chromadb_data"

    # ── LLM (Cloud API — OpenAI-compatible) ──────────────────────
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = "https://api.groq.com/openai/v1"
    LLM_MODEL_NAME: str = "llama-3.1-70b-versatile"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 4096

    # ── Embeddings ───────────────────────────────────────────────
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # ── File Upload ──────────────────────────────────────────────
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: str = "pdf,epub,md"  # comma-separated

    # ── RAG ──────────────────────────────────────────────────────
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 5

    # ── Memory ───────────────────────────────────────────────────
    MAX_SESSION_MESSAGES: int = 20

    # ── Reflection ───────────────────────────────────────────────
    MAX_REFLECTION_LOOPS: int = 3

    # ── Frontend ─────────────────────────────────────────────────
    FRONTEND_URL: str = "http://localhost:5173"

    @property
    def allowed_extensions_list(self) -> list[str]:
        """Parse comma-separated extensions into a list."""
        return [ext.strip().lower() for ext in self.ALLOWED_EXTENSIONS.split(",")]

    @property
    def upload_path(self) -> Path:
        """Get upload directory as a Path object, creating it if needed."""
        path = Path(self.UPLOAD_DIR)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def chromadb_path_resolved(self) -> Path:
        """Get ChromaDB directory as a Path object, creating it if needed."""
        path = Path(self.CHROMADB_PATH)
        path.mkdir(parents=True, exist_ok=True)
        return path

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore",
    }


settings = Settings()
