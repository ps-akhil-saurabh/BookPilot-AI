"""
BookPilot AI — Security Utilities

File validation, path sanitization, and input security.
Authentication is NOT included in Version 1.
"""

import os
import re
from pathlib import Path
from app.core.config import settings
from app.core.exceptions import InvalidFileTypeException, FileTooLargeException


def validate_file_type(filename: str) -> str:
    """
    Validate that the file extension is in the allowed list.
    Returns the normalized extension.
    """
    if not filename or "." not in filename:
        raise InvalidFileTypeException("unknown")

    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in settings.allowed_extensions_list:
        raise InvalidFileTypeException(ext)

    return ext


def validate_file_size(size_bytes: int) -> None:
    """Validate that the file doesn't exceed the maximum upload size."""
    size_mb = size_bytes / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise FileTooLargeException(size_mb, settings.MAX_UPLOAD_SIZE_MB)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent directory traversal and special characters.
    """
    # Remove directory components
    filename = os.path.basename(filename)

    # Remove special characters, keep alphanumeric, dots, hyphens, underscores
    filename = re.sub(r"[^\w\-.]", "_", filename)

    # Remove leading dots (hidden files)
    filename = filename.lstrip(".")

    # Ensure non-empty
    if not filename:
        filename = "unnamed_file"

    return filename


def validate_path_safety(path: str, allowed_root: Path) -> Path:
    """
    Ensure the resolved path stays within the allowed directory.
    Prevents directory traversal attacks.
    """
    resolved = Path(path).resolve()
    allowed = allowed_root.resolve()

    if not str(resolved).startswith(str(allowed)):
        raise ValueError(f"Path traversal detected: {path}")

    return resolved
