"""Pydantic models for GitHub Actions Permissions."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

__all__ = [
    "ModelPermissionLevel",
    "PermissionAccess",
    "PermissionLevel",
    "Permissions",
    "PermissionsEvent",
]


# =============================================================================
# Base Models
# =============================================================================


class StrictModel(BaseModel):
    """Base model with strict configuration."""

    model_config = ConfigDict(extra="forbid")


# =============================================================================
# Enums
# =============================================================================


class PermissionLevel(str, Enum):
    """Permission access levels for GITHUB_TOKEN."""

    READ = "read"
    WRITE = "write"
    NONE = "none"


class PermissionAccess(str, Enum):
    """Global permission access shortcuts."""

    READ_ALL = "read-all"
    WRITE_ALL = "write-all"


class ModelPermissionLevel(str, Enum):
    """Permission levels for models (restricted to read/none)."""

    READ = "read"
    NONE = "none"


# =============================================================================
# Permissions
# =============================================================================


class PermissionsEvent(StrictModel):
    """Fine-grained permissions for GITHUB_TOKEN.

    You can modify the default permissions granted to the GITHUB_TOKEN,
    adding or removing access as required, so that you only allow the
    minimum required access.

    Reference: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#permissions
    """

    actions: PermissionLevel | None = None
    attestations: PermissionLevel | None = None
    checks: PermissionLevel | None = None
    contents: PermissionLevel | None = None
    deployments: PermissionLevel | None = None
    discussions: PermissionLevel | None = None
    id_token: PermissionLevel | None = Field(default=None, alias="id-token")
    issues: PermissionLevel | None = None
    models: ModelPermissionLevel | None = None
    packages: PermissionLevel | None = None
    pages: PermissionLevel | None = None
    pull_requests: PermissionLevel | None = Field(default=None, alias="pull-requests")
    repository_projects: PermissionLevel | None = Field(default=None, alias="repository-projects")
    security_events: PermissionLevel | None = Field(default=None, alias="security-events")
    statuses: PermissionLevel | None = None

    @model_validator(mode="after")
    def check_contents_read(self) -> PermissionsEvent:
        """Validate that 'contents: read' is set when customizing permissions."""
        if self.contents != PermissionLevel.READ:
            message = "must set 'contents: read' when customizing permissions"
            raise ValueError(message)
        return self


Permissions = PermissionAccess | PermissionsEvent
"""
Permissions can be either a global access level ('read-all' or 'write-all')
or fine-grained per-scope permissions.
"""
