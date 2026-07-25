"""
BookPilot AI — Structured Logging

Uses loguru for structured, colorized logging with file rotation.
"""

import sys
from pathlib import Path
from loguru import logger


def setup_logging(debug: bool = False) -> None:
    """
    Configure application logging.

    - Console: colorized, INFO (or DEBUG in debug mode)
    - File: rotated at 10 MB, retained for 7 days, compressed
    """
    # Remove default handler
    logger.remove()

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # Console handler
    logger.add(
        sys.stdout,
        format=log_format,
        level="DEBUG" if debug else "INFO",
        colorize=True,
    )

    # File handler
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger.add(
        str(log_dir / "bookpilot.log"),
        format=log_format,
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        enqueue=True,  # thread-safe
    )

    # Agent-specific log
    logger.add(
        str(log_dir / "agents.log"),
        format=log_format,
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        filter=lambda record: "agent" in record["extra"],
        enqueue=True,
    )

    logger.info("Logging initialized")


# Pre-configured loggers for different components
def get_agent_logger(agent_name: str):
    """Get a logger bound to a specific agent context."""
    return logger.bind(agent=agent_name)


def get_mcp_logger(tool_name: str):
    """Get a logger bound to a specific MCP tool context."""
    return logger.bind(mcp_tool=tool_name)


# Re-export logger for convenience
__all__ = ["logger", "setup_logging", "get_agent_logger", "get_mcp_logger"]
