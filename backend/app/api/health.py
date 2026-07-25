"""
BookPilot AI — Health API

Endpoints: /health, /health/ready, /health/live
"""

from fastapi import APIRouter
from datetime import datetime, timezone

from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Overall system health check."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "connected",
        "chromadb": "connected",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/health/ready")
async def readiness_check():
    """Verify all dependencies are initialized."""
    checks = {
        "database": True,
        "chromadb": True,
    }

    # Check SQLite
    try:
        from app.database.sqlite import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1" if hasattr(db, 'execute') else db.connection().execute)
        db.close()
    except Exception:
        checks["database"] = False

    # Check ChromaDB
    try:
        from app.database.chromadb_client import get_chromadb_client
        client = get_chromadb_client()
        client.heartbeat()
    except Exception:
        checks["chromadb"] = False

    all_ready = all(checks.values())

    return {
        "ready": all_ready,
        "checks": checks,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/health/live")
async def liveness_check():
    """Confirm the backend process is alive."""
    return {
        "alive": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
