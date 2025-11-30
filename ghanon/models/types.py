"""Common type aliases for GitHub Actions Workflow models."""

from typing import Annotated

from pydantic import Field

__all__ = [
    "EnvMapping",
    "EnvVarValue",
    "ExpressionSyntax",
    "Globs",
    "JobName",
    "StringContainingExpression",
]


ExpressionSyntax = Annotated[str, Field(pattern=r"^\$\{\{(.|\r|\n)*\}\}$")]
"""GitHub Actions expression syntax: ${{ ... }}"""

StringContainingExpression = Annotated[str, Field(pattern=r"^.*\$\{\{(.|\r|\n)*\}\}.*$")]
"""String containing GitHub Actions expression syntax."""

JobName = Annotated[str, Field(pattern=r"^[_a-zA-Z][a-zA-Z0-9_-]*$")]
"""Valid job/input identifier: starts with letter or underscore, contains alphanumeric, dash, or underscore."""

EnvVarValue = str | int | float | bool
"""Valid types for environment variable values."""

EnvMapping = dict[str, EnvVarValue] | StringContainingExpression
"""
Environment variables mapping.

To set custom environment variables, you need to specify the variables in the workflow file.
You can define environment variables for a step, job, or entire workflow using the
jobs.<job_id>.steps[*].env, jobs.<job_id>.env, and env keywords.

Reference: https://docs.github.com/en/actions/learn-github-actions/environment-variables
"""

Globs = Annotated[list[str], Field(min_length=1)]
"""Array of glob patterns with at least one item."""
