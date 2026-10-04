"""Logging setup for scripts and pipelines."""

from __future__ import annotations

import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure a single process-wide log format."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        force=True,
    )
