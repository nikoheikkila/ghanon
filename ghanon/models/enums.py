"""Enumerations for GitHub Actions workflow models."""

from __future__ import annotations

from enum import StrEnum

__all__ = [
    "ShellType",
]


class ShellType(StrEnum):
    """Built-in shell types."""

    BASH = "bash"
    PWSH = "pwsh"
    PYTHON = "python"
    SH = "sh"
    CMD = "cmd"
    POWERSHELL = "powershell"
