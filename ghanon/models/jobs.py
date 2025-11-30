"""Job-related Pydantic models for GitHub Actions Workflows."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import Field, field_validator

from .base import StrictModel
from .concurrency import Concurrency
from .container import Container
from .defaults import Defaults
from .environment import Environment
from .matrix import Strategy
from .runner import RunsOn
from .step import Step
from .types import EnvMapping, ExpressionSyntax, JobName

__all__ = [
    "Job",
    "JobNeeds",
    "NormalJob",
    "ReusableWorkflowCallJob",
    "Step",
]


# =============================================================================
# Job Needs
# =============================================================================

JobNeeds = JobName | Annotated[list[JobName], Field(min_length=1)]
"""
Jobs that must complete successfully before this job will run.

It can be a string or array of strings. If a job fails, all jobs that need it
are skipped unless the jobs use a conditional statement that causes the job to continue.

Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idneeds
"""


# =============================================================================
# Jobs
# =============================================================================


class NormalJob(StrictModel):
    """Standard job definition.

    Each job must have an id to associate with the job. The key job_id is a string
    and its value is a map of the job's configuration data. You must replace <job_id>
    with a string that is unique to the jobs object. The <job_id> must start with a
    letter or _ and contain only alphanumeric characters, -, or _.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_id
    """

    name: str | None = Field(
        default=None,
        description="The name of the job displayed on GitHub.",
    )
    needs: JobNeeds | None = None
    permissions: Any | None = None  # Using Any to avoid circular import with Permissions
    runs_on: RunsOn = Field(
        ...,
        alias="runs-on",
        description="The type of machine to run the job on.",
    )
    environment: str | Environment | None = Field(
        default=None,
        description="The environment that the job references.",
    )
    outputs: dict[str, str] | None = Field(
        default=None,
        description=(
            "A map of outputs for a job. Job outputs are available to all downstream jobs that depend on this job."
        ),
    )
    env: EnvMapping | None = Field(
        default=None,
        description="A map of environment variables that are available to all steps in the job.",
    )
    defaults: Defaults | None = Field(
        default=None,
        description="A map of default settings that will apply to all steps in the job.",
    )
    if_: bool | int | float | str | None = Field(
        default=None,
        alias="if",
        description=(
            "You can use the if conditional to prevent a job from running unless a condition is met. "
            "You can use any supported context and expression to create a conditional.\n"
            "Expressions in an if conditional do not require the ${{ }} syntax."
        ),
    )
    steps: Annotated[list[Step], Field(min_length=1)] | None = Field(
        default=None,
        description="A job contains a sequence of tasks called steps.",
    )
    timeout_minutes: int | float | ExpressionSyntax = Field(
        default=360,
        alias="timeout-minutes",
        description=(
            "The maximum number of minutes to let a workflow run before GitHub automatically cancels it. Default: 360"
        ),
    )
    strategy: Strategy | None = Field(
        default=None,
        description="A strategy creates a build matrix for your jobs.",
    )
    continue_on_error: bool | ExpressionSyntax | None = Field(
        default=None,
        alias="continue-on-error",
        description=(
            "Prevents a workflow run from failing when a job fails. "
            "Set to true to allow a workflow run to pass when this job fails."
        ),
    )
    container: str | Container | None = Field(
        default=None,
        description=(
            "A container to run any steps in a job that don't already specify a container. "
            "If you have steps that use both script and container actions, the container actions "
            "will run as sibling containers on the same network with the same volume mounts."
        ),
    )
    services: dict[str, Container] | None = Field(
        default=None,
        description=(
            "Additional containers to host services for a job in a workflow. "
            "These are useful for creating databases or cache services like redis."
        ),
    )
    concurrency: str | Concurrency | None = Field(
        default=None,
        description=(
            "Concurrency ensures that only a single job or workflow using the same concurrency group "
            "will run at a time."
        ),
    )


class ReusableWorkflowCallJob(StrictModel):
    """Job that calls a reusable workflow.

    Reference: https://docs.github.com/en/actions/learn-github-actions/reusing-workflows#calling-a-reusable-workflow
    """

    name: str | None = Field(
        default=None,
        description="The name of the job displayed on GitHub.",
    )
    needs: JobNeeds | None = None
    permissions: Any | None = None  # Using Any to avoid circular import with Permissions
    if_: bool | int | float | str | None = Field(
        default=None,
        alias="if",
        description="You can use the if conditional to prevent a job from running unless a condition is met.",
    )
    uses: Annotated[str, Field(pattern=r"^(.+\/)+(.+)\.(ya?ml)(@.+)?$")] = Field(
        ...,
        description=(
            "The location and version of a reusable workflow file to run as a job, "
            "of the form './{path/to}/{localfile}.yml' or '{owner}/{repo}/{path}/{filename}@{ref}'. "
            "{ref} can be a SHA, a release tag, or a branch name. Using the commit SHA is the safest "
            "for stability and security."
        ),
    )
    with_: EnvMapping | None = Field(
        default=None,
        alias="with",
        description=(
            "A map of inputs that are passed to the called workflow. Any inputs that you pass "
            "must match the input specifications defined in the called workflow. Unlike "
            "'jobs.<job_id>.steps[*].with', the inputs you pass with 'jobs.<job_id>.with' "
            "are not available as environment variables in the called workflow. Instead, "
            "you can reference the inputs by using the inputs context."
        ),
    )
    secrets: EnvMapping | Literal["inherit"] | None = Field(
        default=None,
        description=(
            "When a job is used to call a reusable workflow, you can use 'secrets' to provide "
            "a map of secrets that are passed to the called workflow. Any secrets that you pass "
            "must match the names defined in the called workflow."
        ),
    )
    strategy: Strategy | None = Field(
        default=None,
        description="A strategy creates a build matrix for your jobs.",
    )
    concurrency: str | Concurrency | None = Field(
        default=None,
        description=(
            "Concurrency ensures that only a single job or workflow using the same concurrency group "
            "will run at a time."
        ),
    )

    @field_validator("secrets")
    @classmethod
    def validate_secrets(cls, value: EnvMapping | Literal["inherit"] | None) -> EnvMapping | Literal["inherit"] | None:
        """Validate secrets field."""
        if value == "inherit":
            msg = "do not use 'secrets: inherit' as it can be insecure"
            raise ValueError(msg)
        return value


Job = NormalJob | ReusableWorkflowCallJob
"""A job can be either a normal job or a reusable workflow call."""
