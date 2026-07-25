"""
BookPilot AI — Exception Hierarchy & Handlers

Centralized exception handling for the entire application.
Each exception maps to a specific HTTP status code and error code.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone


# ── Base Exception ───────────────────────────────────────────────

class BookPilotException(Exception):
    """Base exception for all BookPilot AI errors."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


# ── Resource Exceptions ──────────────────────────────────────────

class BookNotFoundException(BookPilotException):
    def __init__(self, book_id: int):
        super().__init__(
            message=f"Book with ID {book_id} not found.",
            code="BOOK_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class PlanNotFoundException(BookPilotException):
    def __init__(self, plan_id: int):
        super().__init__(
            message=f"Reading plan with ID {plan_id} not found.",
            code="PLAN_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class DuplicateBookException(BookPilotException):
    def __init__(self, title: str):
        super().__init__(
            message=f"Book '{title}' already exists in your library.",
            code="DUPLICATE_BOOK",
            status_code=status.HTTP_409_CONFLICT,
        )


# ── File Exceptions ──────────────────────────────────────────────

class FileUploadException(BookPilotException):
    def __init__(self, message: str = "File upload failed."):
        super().__init__(
            message=message,
            code="UPLOAD_FAILED",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class InvalidFileTypeException(BookPilotException):
    def __init__(self, file_type: str):
        super().__init__(
            message=f"File type '{file_type}' is not supported. Allowed: pdf, epub, md.",
            code="INVALID_FILE_TYPE",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class FileTooLargeException(BookPilotException):
    def __init__(self, size_mb: float, max_mb: int):
        super().__init__(
            message=f"File size ({size_mb:.1f} MB) exceeds maximum ({max_mb} MB).",
            code="FILE_TOO_LARGE",
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        )


# ── AI / Agent Exceptions ───────────────────────────────────────

class AgentExecutionException(BookPilotException):
    def __init__(self, agent: str, message: str = "Agent execution failed."):
        super().__init__(
            message=f"Agent '{agent}' failed: {message}",
            code="AGENT_EXECUTION_FAILED",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class LLMException(BookPilotException):
    def __init__(self, message: str = "LLM request failed."):
        super().__init__(
            message=message,
            code="LLM_FAILED",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


# ── MCP Exceptions ───────────────────────────────────────────────

class MCPToolException(BookPilotException):
    def __init__(self, tool: str, message: str = "MCP tool invocation failed."):
        super().__init__(
            message=f"MCP tool '{tool}' failed: {message}",
            code="MCP_TOOL_FAILED",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


# ── RAG Exceptions ───────────────────────────────────────────────

class RAGException(BookPilotException):
    def __init__(self, message: str = "RAG retrieval failed."):
        super().__init__(
            message=message,
            code="RAG_FAILED",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class DocumentNotIndexedException(BookPilotException):
    def __init__(self, book_id: int):
        super().__init__(
            message=f"Book {book_id} has not been uploaded/indexed. Please upload the book first.",
            code="DOCUMENT_NOT_INDEXED",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


# ── Validation Exceptions ───────────────────────────────────────

class ValidationException(BookPilotException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


# ── Exception Handlers (registered in main.py) ──────────────────

async def bookpilot_exception_handler(request: Request, exc: BookPilotException):
    """Handle all BookPilot-specific exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "error": {
                "code": exc.code,
                "details": exc.message,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions with a safe generic message."""
    from app.core.config import settings

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An unexpected error occurred.",
            "error": {
                "code": "INTERNAL_ERROR",
                "details": str(exc) if settings.DEBUG else "Internal server error.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
