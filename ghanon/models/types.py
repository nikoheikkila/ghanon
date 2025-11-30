"""Common type aliases for GitHub Actions Workflow models."""

from typing import Annotated

from pydantic import Field

__all__ = [
    "Globs",
]


Globs = Annotated[list[str], Field(min_length=1)]
"""Array of glob patterns with at least one item."""
