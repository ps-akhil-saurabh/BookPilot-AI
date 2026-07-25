"""
BookPilot AI — FastAPI Application Entry Point

Configures:
- CORS middleware
- Exception handlers
- API route registration
- Database initialization
- Lifespan events (startup/shutdown)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logger import setup_logging, logger
from app.core.exceptions import (
    BookPilotException,
    bookpilot_exception_handler,
    general_exception_handler,
)
from app.database.sqlite import init_db
from app.database.chromadb_client import init_chromadb


# ── Lifespan ─────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # ── Startup ──────────────────────────────────────────────
    setup_logging(debug=settings.DEBUG)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"API prefix: {settings.API_PREFIX}")

    # Initialize databases
    init_db()
    init_chromadb()

    # Ensure upload directory exists
    settings.upload_path

    logger.info("Application startup complete")

    yield

    # ── Shutdown ─────────────────────────────────────────────
    logger.info("Application shutting down")


# ── App ──────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "An autonomous AI Reading Mentor that plans personalized reading schedules, "
        "adapts to missed sessions, explains difficult concepts, quizzes users for "
        "retention, tracks long-term progress, and continuously improves reading plans."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ── CORS ─────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Exception Handlers ──────────────────────────────────────────

app.add_exception_handler(BookPilotException, bookpilot_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


# ── API Routes ───────────────────────────────────────────────────

from app.api import books, health, planner, reading, upload, learning, analytics, workflow  # noqa: E402

app.include_router(books.router, prefix=settings.API_PREFIX, tags=["Books"])
app.include_router(health.router, prefix=settings.API_PREFIX, tags=["Health"])
app.include_router(planner.router, prefix=settings.API_PREFIX, tags=["Planner"])
app.include_router(reading.router, prefix=settings.API_PREFIX, tags=["Reading"])
app.include_router(upload.router, prefix=settings.API_PREFIX, tags=["Upload"])
app.include_router(learning.router, prefix=settings.API_PREFIX, tags=["Learning"])
app.include_router(analytics.router, prefix=settings.API_PREFIX, tags=["Analytics"])
app.include_router(workflow.router, prefix=settings.API_PREFIX, tags=["Workflow"])


# ── Root ─────────────────────────────────────────────────────────

@app.get("/", tags=["Root"])
async def root():
    """Application root endpoint."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": f"{settings.API_PREFIX}/health",
    }
