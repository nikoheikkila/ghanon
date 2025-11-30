"""Job-related Pydantic models for GitHub Actions Workflows."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .concurrency import Concurrency
from .container import Container
from .defaults import Defaults, ShellType
from .environment import Environment

__all__ = [
    "Configuration",
    "Job",
    "JobName",
    "JobNeeds",
    "Matrix",
    "MatrixIncludeExclude",
    "NormalJob",
    "ReusableWorkflowCallJob",
    "RunnerGroup",
    "RunsOn",
    "Step",
    "Strategy",
]


# =============================================================================
# Type Aliases
# =============================================================================

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

Configuration = str | int | float | bool | dict[str, Any] | list[Any]
"""Recursive configuration type for matrix values."""

MatrixIncludeExclude = ExpressionSyntax | list[dict[str, Configuration]]
"""Include/exclude entries in a matrix."""


# =============================================================================
# Base Models
# =============================================================================


class StrictModel(BaseModel):
    """Base model with strict configuration."""

    model_config = ConfigDict(extra="forbid")


class FlexibleModel(BaseModel):
    """Base model allowing additional properties."""

    model_config = ConfigDict(extra="allow")


# =============================================================================
# Step
# =============================================================================


class Step(StrictModel):
    """A single step in a job.

    Steps can run commands, run setup tasks, or run an action in your repository,
    a public repository, or an action published in a Docker registry.
    Not all steps run actions, but all actions run as a step.

    Each step runs in its own process in the virtual environment and has access
    to the workspace and filesystem. Because steps run in their own process,
    changes to environment variables are not preserved between steps.

    Must contain either `uses` or `run`.

    Reference: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idsteps
    """

    id: str | None = Field(
        default=None,
        description=(
            "A unique identifier for the step. You can use the id to reference the step in contexts. "
            "For more information, see https://help.github.com/en/articles/contexts-and-expression-syntax-for-github-actions."
        ),
    )
    if_: bool | int | float | str | None = Field(
        default=None,
        alias="if",
        description=(
            "You can use the if conditional to prevent a step from running unless a condition is met. "
            "You can use any supported context and expression to create a conditional.\n"
            "Expressions in an if conditional do not require the ${{ }} syntax. "
            "For more information, see https://help.github.com/en/articles/contexts-and-expression-syntax-for-github-actions."
        ),
    )
    name: str | None = Field(
        default=None,
        description="A name for your step to display on GitHub.",
    )
    uses: str | None = Field(
        default=None,
        description=(
            "Selects an action to run as part of a step in your job. An action is a reusable unit of code. "
            "You can use an action defined in the same repository as the workflow, a public repository, "
            "or in a published Docker container image (https://hub.docker.com/).\n\n"
            "We strongly recommend that you include the version of the action you are using by specifying "
            "a Git ref, SHA, or Docker tag number. If you don't specify a version, it could break your "
            "workflows or cause unexpected behavior when the action owner publishes an update.\n\n"
            "- Using the commit SHA of a released action version is the safest for stability and security.\n"
            "- Using the specific major action version allows you to receive critical fixes and security patches.\n"
            "- Using the master branch of an action may be convenient, but if someone releases a new major version "
            "with a breaking change, your workflow could break."
        ),
    )
    run: str | None = Field(
        default=None,
        description=(
            "Runs command-line programs using the operating system's shell. If you do not provide a name, "
            "the step name will default to the text specified in the run command.\n\n"
            "Commands run using non-login shells by default. You can choose a different shell and "
            "customize the shell used to run commands.\n\n"
            "Each run keyword represents a new process and shell in the virtual environment. "
            "When you provide multi-line commands, each line runs in the same shell."
        ),
    )
    working_directory: str | None = Field(
        default=None,
        alias="working-directory",
        description=(
            "Using the working-directory keyword, you can specify the working directory of where to run the command."
        ),
    )
    shell: str | ShellType | None = Field(
        default=None,
        description=(
            "You can override the default shell settings in the runner's operating system using the shell keyword."
        ),
    )
    with_: EnvMapping | None = Field(
        default=None,
        alias="with",
        description=(
            "A map of the input parameters defined by the action. Each input parameter is a key/value pair. "
            "Input parameters are set as environment variables. The variable is prefixed with INPUT_ and "
            "converted to upper case."
        ),
    )
    env: EnvMapping | None = Field(
        default=None,
        description=(
            "Sets environment variables for steps to use in the virtual environment. "
            "You can also set environment variables for the entire workflow or a job."
        ),
    )
    continue_on_error: bool | ExpressionSyntax = Field(
        default=False,
        alias="continue-on-error",
        description=(
            "Prevents a job from failing when a step fails. Set to true to allow a job to pass when this step fails."
        ),
    )
    timeout_minutes: int | float | ExpressionSyntax | None = Field(
        default=None,
        alias="timeout-minutes",
        description="The maximum number of minutes to run the step before killing the process.",
    )

    @model_validator(mode="after")
    def check_uses_or_run(self) -> Step:
        """Validate that step has either uses or run but not both."""
        if self.uses is None and self.run is None:
            msg = "Step must contain either 'uses' or 'run'"
            raise ValueError(msg)
        if self.uses is not None and self.run is not None:
            msg = "Step cannot contain both 'uses' and 'run'"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def check_run_dependencies(self) -> Step:
        """Validate that shell and working-directory are only used with run."""
        if self.run is None:
            if self.working_directory is not None:
                msg = "'working-directory' requires 'run' to be specified"
                raise ValueError(msg)
            if self.shell is not None:
                msg = "'shell' requires 'run' to be specified"
                raise ValueError(msg)
        return self


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


# =============================================================================
# Runner Configuration
# =============================================================================


class RunnerGroup(BaseModel):
    """Runner group configuration for choosing runners in a group."""

    group: str | None = None
    labels: str | list[str] | None = None


RunsOn = str | list[str] | RunnerGroup | StringContainingExpression | ExpressionSyntax
"""
The type of machine to run the job on.

The machine can be either a GitHub-hosted runner or a self-hosted runner.

Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idruns-on
"""


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
