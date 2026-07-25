"""
BookPilot AI — Common Schemas

Standard response wrappers used across all API endpoints.
"""

from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime, timezone


class StandardResponse(BaseModel):
    """Standard success response wrapper matching the API Specification Document."""
    success: bool = True
    message: str = "Operation completed successfully."
    data: Any = None
    timestamp: datetime = None

    def model_post_init(self, __context):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)


class ErrorDetail(BaseModel):
    """Error detail object."""
    code: str
    details: str


class ErrorResponse(BaseModel):
    """Standard error response wrapper."""
    success: bool = False
    message: str
    error: ErrorDetail
    timestamp: datetime = None

    def model_post_init(self, __context):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    skip: int = 0
    limit: int = 100
