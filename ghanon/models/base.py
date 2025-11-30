"""Base models for GitHub Actions Workflows."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

__all__ = ["FlexibleModel", "StrictModel"]


class StrictModel(BaseModel):
    """Base model with strict configuration."""

    model_config = ConfigDict(extra="forbid")


class FlexibleModel(BaseModel):
    """Base model allowing additional properties."""

    model_config = ConfigDict(extra="allow")
