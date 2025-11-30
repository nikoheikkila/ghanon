"""Environment model for GitHub Actions workflows."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

__all__ = ["Environment"]


class StrictModel(BaseModel):
    """Base model with strict configuration."""

    model_config = ConfigDict(extra="forbid")


class Environment(StrictModel):
    """The environment that the job references.

    Reference: https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions#jobsjob_idenvironment
    """

    name: str = Field(
        ...,
        description="The name of the environment configured in the repo.",
    )
    url: str | None = Field(
        default=None,
        description="A deployment URL",
    )
