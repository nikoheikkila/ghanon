"""Matrix and Strategy models for GitHub Actions Workflows."""

from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from .base import FlexibleModel, StrictModel

__all__ = [
    "Configuration",
    "Matrix",
    "MatrixIncludeExclude",
    "Strategy",
]


# =============================================================================
# Type Aliases
# =============================================================================

ExpressionSyntax = Annotated[str, Field(pattern=r"^\$\{\{(.|\r|\n)*\}\}$")]
"""GitHub Actions expression syntax: ${{ ... }}"""

Configuration = str | int | float | bool | dict[str, Any] | list[Any]
"""Recursive configuration type for matrix values."""

MatrixIncludeExclude = ExpressionSyntax | list[dict[str, Configuration]]
"""Include/exclude entries in a matrix."""


# =============================================================================
# Matrix Strategy
# =============================================================================


class Matrix(FlexibleModel):
    """Build matrix configuration.

    A build matrix is a set of different configurations of the virtual environment.
    For example you might run a job against more than one supported version of a language,
    operating system, or tool. Each configuration is a copy of the job that runs and reports a status.

    Reference: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idstrategymatrix
    """

    include: MatrixIncludeExclude | None = None
    exclude: MatrixIncludeExclude | None = None

    # Additional matrix dimensions are allowed via extra="allow"


class Strategy(StrictModel):
    """Strategy configuration for a job.

    A strategy creates a build matrix for your jobs. You can define different
    variations of an environment to run each job in.

    Reference: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idstrategy
    """

    matrix: Matrix | ExpressionSyntax = Field(
        ...,
        description="The build matrix configuration.",
    )
    fail_fast: bool | str = Field(
        default=True,
        alias="fail-fast",
        description="When set to true, GitHub cancels all in-progress jobs if any matrix job fails. Default: true",
    )
    max_parallel: int | float | str | None = Field(
        default=None,
        alias="max-parallel",
        description=(
            "The maximum number of jobs that can run simultaneously when using a matrix job strategy. "
            "By default, GitHub will maximize the number of jobs run in parallel depending on the "
            "available runners on GitHub-hosted virtual machines."
        ),
    )
