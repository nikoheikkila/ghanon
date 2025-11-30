"""
Pydantic models for GitHub Actions Workflow schema.

Based on: https://json.schemastore.org/github-workflow.json
Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions
"""

from __future__ import annotations

from enum import Enum
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


__all__ = [
    # Main workflow model
    "Workflow",
    "parse_workflow",
    "parse_workflow_yaml",
    # Job models
    "Job",
    "NormalJob",
    "ReusableWorkflowCallJob",
    # Step model
    "Step",
    # Supporting models
    "Concurrency",
    "Container",
    "ContainerCredentials",
    "Defaults",
    "DefaultsRun",
    "Environment",
    "Matrix",
    "Permissions",
    "PermissionsEvent",
    "RunnerGroup",
    "Strategy",
    # Event models
    "On",
    "OnConfiguration",
    "BranchProtectionRuleEvent",
    "CheckRunEvent",
    "CheckSuiteEvent",
    "DiscussionEvent",
    "DiscussionCommentEvent",
    "IssueCommentEvent",
    "IssuesEvent",
    "LabelEvent",
    "MergeGroupEvent",
    "MilestoneEvent",
    "ProjectEvent",
    "ProjectCardEvent",
    "ProjectColumnEvent",
    "PullRequestEvent",
    "PullRequestTargetEvent",
    "PullRequestReviewEvent",
    "PullRequestReviewCommentEvent",
    "PushEvent",
    "RegistryPackageEvent",
    "ReleaseEvent",
    "ScheduleItem",
    "WorkflowCallEvent",
    "WorkflowDispatchEvent",
    "WorkflowRunEvent",
    # Workflow call/dispatch inputs
    "WorkflowCallInput",
    "WorkflowCallOutput",
    "WorkflowCallSecret",
    "WorkflowDispatchInput",
    # Enums
    "Architecture",
    "EventType",
    "Machine",
    "ModelPermissionLevel",
    "PermissionAccess",
    "PermissionLevel",
    "ShellType",
    "WorkflowCallInputType",
    "WorkflowDispatchInputType",
    # Activity type enums
    "BranchProtectionRuleActivityType",
    "CheckRunActivityType",
    "CheckSuiteActivityType",
    "DiscussionActivityType",
    "DiscussionCommentActivityType",
    "IssueCommentActivityType",
    "IssuesActivityType",
    "LabelActivityType",
    "MergeGroupActivityType",
    "MilestoneActivityType",
    "ProjectActivityType",
    "ProjectCardActivityType",
    "ProjectColumnActivityType",
    "PullRequestActivityType",
    "PullRequestTargetActivityType",
    "PullRequestReviewActivityType",
    "PullRequestReviewCommentActivityType",
    "RegistryPackageActivityType",
    "ReleaseActivityType",
    "WorkflowRunActivityType",
    # Type aliases
    "Configuration",
    "EnvMapping",
    "EnvVarValue",
    "ExpressionSyntax",
    "Globs",
    "JobName",
    "JobNeeds",
    "MatrixIncludeExclude",
    "RunsOn",
    "StringContainingExpression",
]


# =============================================================================
# Enums
# =============================================================================


class Architecture(str, Enum):
    """Supported architectures for runners."""

    ARM32 = "ARM32"
    X64 = "x64"
    X86 = "x86"


class Machine(str, Enum):
    """Supported machine types."""

    LINUX = "linux"
    MACOS = "macos"
    WINDOWS = "windows"


class PermissionLevel(str, Enum):
    """Permission access levels for GITHUB_TOKEN."""

    READ = "read"
    WRITE = "write"
    NONE = "none"


class PermissionAccess(str, Enum):
    """Global permission access shortcuts."""

    READ_ALL = "read-all"
    WRITE_ALL = "write-all"


class ShellType(str, Enum):
    """Built-in shell types."""

    BASH = "bash"
    PWSH = "pwsh"
    PYTHON = "python"
    SH = "sh"
    CMD = "cmd"
    POWERSHELL = "powershell"


class ModelPermissionLevel(str, Enum):
    """Permission levels for models (restricted to read/none)."""

    READ = "read"
    NONE = "none"


class WorkflowDispatchInputType(str, Enum):
    """Input types for workflow_dispatch event."""

    STRING = "string"
    CHOICE = "choice"
    BOOLEAN = "boolean"
    NUMBER = "number"
    ENVIRONMENT = "environment"


class WorkflowCallInputType(str, Enum):
    """Input types for workflow_call event."""

    BOOLEAN = "boolean"
    NUMBER = "number"
    STRING = "string"


class EventType(str, Enum):
    """
    GitHub events that can trigger workflows.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows
    """

    BRANCH_PROTECTION_RULE = "branch_protection_rule"
    CHECK_RUN = "check_run"
    CHECK_SUITE = "check_suite"
    CREATE = "create"
    DELETE = "delete"
    DEPLOYMENT = "deployment"
    DEPLOYMENT_STATUS = "deployment_status"
    DISCUSSION = "discussion"
    DISCUSSION_COMMENT = "discussion_comment"
    FORK = "fork"
    GOLLUM = "gollum"
    ISSUE_COMMENT = "issue_comment"
    ISSUES = "issues"
    LABEL = "label"
    MERGE_GROUP = "merge_group"
    MILESTONE = "milestone"
    PAGE_BUILD = "page_build"
    PROJECT = "project"
    PROJECT_CARD = "project_card"
    PROJECT_COLUMN = "project_column"
    PUBLIC = "public"
    PULL_REQUEST = "pull_request"
    PULL_REQUEST_REVIEW = "pull_request_review"
    PULL_REQUEST_REVIEW_COMMENT = "pull_request_review_comment"
    PULL_REQUEST_TARGET = "pull_request_target"
    PUSH = "push"
    REGISTRY_PACKAGE = "registry_package"
    RELEASE = "release"
    STATUS = "status"
    WATCH = "watch"
    WORKFLOW_CALL = "workflow_call"
    WORKFLOW_DISPATCH = "workflow_dispatch"
    WORKFLOW_RUN = "workflow_run"
    REPOSITORY_DISPATCH = "repository_dispatch"


# =============================================================================
# Activity Type Enums
# =============================================================================


class BranchProtectionRuleActivityType(str, Enum):
    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class CheckRunActivityType(str, Enum):
    CREATED = "created"
    REREQUESTED = "rerequested"
    COMPLETED = "completed"
    REQUESTED_ACTION = "requested_action"


class CheckSuiteActivityType(str, Enum):
    COMPLETED = "completed"
    REQUESTED = "requested"
    REREQUESTED = "rerequested"


class DiscussionActivityType(str, Enum):
    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"
    TRANSFERRED = "transferred"
    PINNED = "pinned"
    UNPINNED = "unpinned"
    LABELED = "labeled"
    UNLABELED = "unlabeled"
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    CATEGORY_CHANGED = "category_changed"
    ANSWERED = "answered"
    UNANSWERED = "unanswered"


class DiscussionCommentActivityType(str, Enum):
    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class IssueCommentActivityType(str, Enum):
    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class IssuesActivityType(str, Enum):
    OPENED = "opened"
    EDITED = "edited"
    DELETED = "deleted"
    TRANSFERRED = "transferred"
    PINNED = "pinned"
    UNPINNED = "unpinned"
    CLOSED = "closed"
    REOPENED = "reopened"
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    LABELED = "labeled"
    UNLABELED = "unlabeled"
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    MILESTONED = "milestoned"
    DEMILESTONED = "demilestoned"


class LabelActivityType(str, Enum):
    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class MergeGroupActivityType(str, Enum):
    CHECKS_REQUESTED = "checks_requested"


class MilestoneActivityType(str, Enum):
    CREATED = "created"
    CLOSED = "closed"
    OPENED = "opened"
    EDITED = "edited"
    DELETED = "deleted"


class ProjectActivityType(str, Enum):
    CREATED = "created"
    UPDATED = "updated"
    CLOSED = "closed"
    REOPENED = "reopened"
    EDITED = "edited"
    DELETED = "deleted"


class ProjectCardActivityType(str, Enum):
    CREATED = "created"
    MOVED = "moved"
    CONVERTED = "converted"
    EDITED = "edited"
    DELETED = "deleted"


class ProjectColumnActivityType(str, Enum):
    CREATED = "created"
    UPDATED = "updated"
    MOVED = "moved"
    DELETED = "deleted"


class PullRequestActivityType(str, Enum):
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    LABELED = "labeled"
    UNLABELED = "unlabeled"
    OPENED = "opened"
    EDITED = "edited"
    CLOSED = "closed"
    REOPENED = "reopened"
    SYNCHRONIZE = "synchronize"
    CONVERTED_TO_DRAFT = "converted_to_draft"
    READY_FOR_REVIEW = "ready_for_review"
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    MILESTONED = "milestoned"
    DEMILESTONED = "demilestoned"
    REVIEW_REQUESTED = "review_requested"
    REVIEW_REQUEST_REMOVED = "review_request_removed"
    AUTO_MERGE_ENABLED = "auto_merge_enabled"
    AUTO_MERGE_DISABLED = "auto_merge_disabled"
    ENQUEUED = "enqueued"
    DEQUEUED = "dequeued"


class PullRequestTargetActivityType(str, Enum):
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    LABELED = "labeled"
    UNLABELED = "unlabeled"
    OPENED = "opened"
    EDITED = "edited"
    CLOSED = "closed"
    REOPENED = "reopened"
    SYNCHRONIZE = "synchronize"
    CONVERTED_TO_DRAFT = "converted_to_draft"
    READY_FOR_REVIEW = "ready_for_review"
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    REVIEW_REQUESTED = "review_requested"
    REVIEW_REQUEST_REMOVED = "review_request_removed"
    AUTO_MERGE_ENABLED = "auto_merge_enabled"
    AUTO_MERGE_DISABLED = "auto_merge_disabled"


class PullRequestReviewActivityType(str, Enum):
    SUBMITTED = "submitted"
    EDITED = "edited"
    DISMISSED = "dismissed"


class PullRequestReviewCommentActivityType(str, Enum):
    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class RegistryPackageActivityType(str, Enum):
    PUBLISHED = "published"
    UPDATED = "updated"


class ReleaseActivityType(str, Enum):
    PUBLISHED = "published"
    UNPUBLISHED = "unpublished"
    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"
    PRERELEASED = "prereleased"
    RELEASED = "released"


class WorkflowRunActivityType(str, Enum):
    REQUESTED = "requested"
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"


# =============================================================================
# Type Aliases
# =============================================================================

Globs = Annotated[list[str], Field(min_length=1)]
"""Array of glob patterns with at least one item."""

ExpressionSyntax = Annotated[str, Field(pattern=r"^\$\{\{(.|\r|\n)*\}\}$")]
"""GitHub Actions expression syntax: ${{ ... }}"""

StringContainingExpression = Annotated[
    str, Field(pattern=r"^.*\$\{\{(.|\r|\n)*\}\}.*$")
]
"""String containing GitHub Actions expression syntax."""

JobName = Annotated[str, Field(pattern=r"^[_a-zA-Z][a-zA-Z0-9_-]*$")]
"""Valid job/input identifier: starts with letter or underscore, contains alphanumeric, dash, or underscore."""


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
# Environment Variables
# =============================================================================

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


# =============================================================================
# Concurrency
# =============================================================================


class Concurrency(StrictModel):
    """
    Concurrency configuration.

    Concurrency ensures that only a single job or workflow using the same
    concurrency group will run at a time.

    Reference: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#example-using-concurrency-to-cancel-any-in-progress-job-or-run-1
    """

    group: str = Field(
        ...,
        description=(
            "When a concurrent job or workflow is queued, if another job or workflow "
            "using the same concurrency group in the repository is in progress, the "
            "queued job or workflow will be pending. Any previously pending job or "
            "workflow in the concurrency group will be canceled."
        ),
    )
    cancel_in_progress: bool | ExpressionSyntax | None = Field(
        default=None,
        alias="cancel-in-progress",
        description="To cancel any currently running job or workflow in the same concurrency group, specify cancel-in-progress: true.",
    )


# =============================================================================
# Permissions
# =============================================================================


class PermissionsEvent(StrictModel):
    """
    Fine-grained permissions for GITHUB_TOKEN.

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
    repository_projects: PermissionLevel | None = Field(
        default=None, alias="repository-projects"
    )
    security_events: PermissionLevel | None = Field(
        default=None, alias="security-events"
    )
    statuses: PermissionLevel | None = None


Permissions = PermissionAccess | PermissionsEvent
"""
Permissions can be either a global access level ('read-all' or 'write-all')
or fine-grained per-scope permissions.
"""


# =============================================================================
# Defaults
# =============================================================================


class DefaultsRun(StrictModel):
    """Default settings for run steps."""

    shell: str | ShellType | None = Field(
        default=None,
        description=(
            "You can override the default shell settings in the runner's operating "
            "system using the shell keyword. You can use built-in shell keywords, "
            "or you can define a custom set of shell options.\n\n"
            "Reference: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsshell"
        ),
    )
    working_directory: str | None = Field(
        default=None,
        alias="working-directory",
        description="Using the working-directory keyword, you can specify the working directory of where to run the command.",
    )

    @model_validator(mode="after")
    def check_at_least_one_property(self) -> DefaultsRun:
        if self.shell is None and self.working_directory is None:
            raise ValueError(
                "At least one of 'shell' or 'working-directory' must be specified"
            )
        return self


class Defaults(StrictModel):
    """
    Default settings that apply to all jobs/steps.

    Reference: https://help.github.com/en/actions/reference/workflow-syntax-for-github-actions#defaults
    """

    run: DefaultsRun | None = None

    @model_validator(mode="after")
    def check_at_least_one_property(self) -> Defaults:
        if self.run is None:
            raise ValueError("At least one property must be specified in defaults")
        return self


# =============================================================================
# Container
# =============================================================================


class ContainerCredentials(BaseModel):
    """Container registry credentials for docker login."""

    username: str | None = None
    password: str | None = None


class Container(StrictModel):
    """
    Container configuration for running jobs.

    Reference: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idcontainer
    """

    image: str = Field(
        ...,
        description="The Docker image to use as the container to run the action. The value can be the Docker Hub image name or a registry name.",
    )
    credentials: ContainerCredentials | None = Field(
        default=None,
        description=(
            "If the image's container registry requires authentication to pull the image, "
            "you can use credentials to set a map of the username and password. "
            "The credentials are the same values that you would provide to the `docker login` command.\n\n"
            "Reference: https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions#jobsjob_idcontainercredentials"
        ),
    )
    env: EnvMapping | None = Field(
        default=None,
        description="Sets an array of environment variables in the container.",
    )
    ports: Annotated[list[int | str], Field(min_length=1)] | None = Field(
        default=None,
        description="Sets an array of ports to expose on the container.",
    )
    volumes: Annotated[list[str], Field(min_length=1)] | None = Field(
        default=None,
        description=(
            "Sets an array of volumes for the container to use. You can use volumes to share data "
            "between services or other steps in a job. You can specify named Docker volumes, "
            "anonymous Docker volumes, or bind mounts on the host.\n"
            "To specify a volume, you specify the source and destination path: <source>:<destinationPath>\n"
            "The <source> is a volume name or an absolute path on the host machine, "
            "and <destinationPath> is an absolute path in the container."
        ),
    )
    options: str | None = Field(
        default=None,
        description=(
            "Additional Docker container resource options. "
            "For a list of options, see https://docs.docker.com/engine/reference/commandline/create/#options."
        ),
    )


# =============================================================================
# Environment
# =============================================================================


class Environment(StrictModel):
    """
    The environment that the job references.

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


# =============================================================================
# Step
# =============================================================================


class Step(StrictModel):
    """
    A single step in a job.

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
        description="Using the working-directory keyword, you can specify the working directory of where to run the command.",
    )
    shell: str | ShellType | None = Field(
        default=None,
        description="You can override the default shell settings in the runner's operating system using the shell keyword.",
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
        description="Prevents a job from failing when a step fails. Set to true to allow a job to pass when this step fails.",
    )
    timeout_minutes: int | float | ExpressionSyntax | None = Field(
        default=None,
        alias="timeout-minutes",
        description="The maximum number of minutes to run the step before killing the process.",
    )

    @model_validator(mode="after")
    def check_uses_or_run(self) -> Step:
        if self.uses is None and self.run is None:
            raise ValueError("Step must contain either 'uses' or 'run'")
        if self.uses is not None and self.run is not None:
            raise ValueError("Step cannot contain both 'uses' and 'run'")
        return self

    @model_validator(mode="after")
    def check_run_dependencies(self) -> Step:
        if self.run is None:
            if self.working_directory is not None:
                raise ValueError("'working-directory' requires 'run' to be specified")
            if self.shell is not None:
                raise ValueError("'shell' requires 'run' to be specified")
        return self


# =============================================================================
# Matrix Strategy
# =============================================================================

Configuration = str | int | float | bool | dict[str, Any] | list[Any]
"""Recursive configuration type for matrix values."""

MatrixIncludeExclude = ExpressionSyntax | list[dict[str, Configuration]]
"""Include/exclude entries in a matrix."""


class Matrix(FlexibleModel):
    """
    Build matrix configuration.

    A build matrix is a set of different configurations of the virtual environment.
    For example you might run a job against more than one supported version of a language,
    operating system, or tool. Each configuration is a copy of the job that runs and reports a status.

    Reference: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idstrategymatrix
    """

    include: MatrixIncludeExclude | None = None
    exclude: MatrixIncludeExclude | None = None

    # Additional matrix dimensions are allowed via extra="allow"


class Strategy(StrictModel):
    """
    Strategy configuration for a job.

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
    """
    Standard job definition.

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
    permissions: Permissions | None = None
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
            "A map of outputs for a job. Job outputs are available to all downstream "
            "jobs that depend on this job."
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
        description="The maximum number of minutes to let a workflow run before GitHub automatically cancels it. Default: 360",
    )
    strategy: Strategy | None = Field(
        default=None,
        description="A strategy creates a build matrix for your jobs.",
    )
    continue_on_error: bool | ExpressionSyntax | None = Field(
        default=None,
        alias="continue-on-error",
        description="Prevents a workflow run from failing when a job fails. Set to true to allow a workflow run to pass when this job fails.",
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
        description="Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time.",
    )


class ReusableWorkflowCallJob(StrictModel):
    """
    Job that calls a reusable workflow.

    Reference: https://docs.github.com/en/actions/learn-github-actions/reusing-workflows#calling-a-reusable-workflow
    """

    name: str | None = Field(
        default=None,
        description="The name of the job displayed on GitHub.",
    )
    needs: JobNeeds | None = None
    permissions: Permissions | None = None
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
        description="Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time.",
    )


Job = NormalJob | ReusableWorkflowCallJob
"""A job can be either a normal job or a reusable workflow call."""


# =============================================================================
# Workflow Dispatch Input
# =============================================================================


class WorkflowDispatchInput(StrictModel):
    """
    Input parameter for workflow_dispatch event.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/metadata-syntax-for-github-actions#inputsinput_id
    """

    description: str = Field(
        ...,
        description="A string description of the input parameter.",
    )
    deprecation_message: str | None = Field(
        default=None,
        alias="deprecationMessage",
        description="A string shown to users using the deprecated input.",
    )
    required: bool | None = Field(
        default=None,
        description="A boolean to indicate whether the action requires the input parameter.",
    )
    default: str | bool | int | float | None = Field(
        default=None,
        description="The default value is used when an input parameter isn't specified in a workflow file.",
    )
    type: WorkflowDispatchInputType | None = Field(
        default=None,
        description="A string representing the type of the input.",
    )
    options: Annotated[list[str], Field(min_length=1)] | None = Field(
        default=None,
        description="The options of the dropdown list, if the type is a choice.",
    )

    @model_validator(mode="after")
    def validate_type_constraints(self) -> WorkflowDispatchInput:
        if self.type == WorkflowDispatchInputType.CHOICE and self.options is None:
            raise ValueError("'options' is required when type is 'choice'")
        return self


# =============================================================================
# Workflow Call Input/Output/Secret
# =============================================================================


class WorkflowCallInput(StrictModel):
    """Input parameter for workflow_call event."""

    description: str | None = Field(
        default=None,
        description="A string description of the input parameter.",
    )
    required: bool | None = Field(
        default=None,
        description="A boolean to indicate whether the action requires the input parameter.",
    )
    type: WorkflowCallInputType = Field(
        ...,
        description="The data type of the input. This must be one of: boolean, number, or string.",
    )
    default: bool | int | float | str | None = Field(
        default=None,
        description="The default value is used when an input parameter isn't specified in a workflow file.",
    )


class WorkflowCallOutput(StrictModel):
    """Output for workflow_call event."""

    description: str | None = Field(
        default=None,
        description="A string description of the output parameter.",
    )
    value: str = Field(
        ...,
        description=(
            "The value that the output parameter will be mapped to. You can set this to a string "
            "or an expression with context. For example, you can use the steps context to set "
            "the value of an output to the output value of a step."
        ),
    )


class WorkflowCallSecret(StrictModel):
    """Secret definition for workflow_call event."""

    description: str | None = Field(
        default=None,
        description="A string description of the secret parameter.",
    )
    required: bool | None = Field(
        default=None,
        description="A boolean specifying whether the secret must be supplied.",
    )


# =============================================================================
# Event Configurations
# =============================================================================


class BranchProtectionRuleEvent(FlexibleModel):
    """
    Branch protection rule event configuration.

    Runs your workflow anytime the branch_protection_rule event occurs.

    Reference: https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#branch_protection_rule
    """

    types: (
        list[BranchProtectionRuleActivityType] | BranchProtectionRuleActivityType | None
    ) = None


class CheckRunEvent(FlexibleModel):
    """
    Check run event configuration.

    Runs your workflow anytime the check_run event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#check-run-event-check_run
    """

    types: list[CheckRunActivityType] | CheckRunActivityType | None = None


class CheckSuiteEvent(FlexibleModel):
    """
    Check suite event configuration.

    Runs your workflow anytime the check_suite event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#check-suite-event-check_suite
    """

    types: list[CheckSuiteActivityType] | CheckSuiteActivityType | None = None


class DiscussionEvent(FlexibleModel):
    """
    Discussion event configuration.

    Runs your workflow anytime the discussion event occurs.

    Reference: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#discussion
    """

    types: list[DiscussionActivityType] | DiscussionActivityType | None = None


class DiscussionCommentEvent(FlexibleModel):
    """
    Discussion comment event configuration.

    Reference: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#discussion_comment
    """

    types: (
        list[DiscussionCommentActivityType] | DiscussionCommentActivityType | None
    ) = None


class IssueCommentEvent(FlexibleModel):
    """
    Issue comment event configuration.

    Runs your workflow anytime the issue_comment event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#issue-comment-event-issue_comment
    """

    types: list[IssueCommentActivityType] | IssueCommentActivityType | None = None


class IssuesEvent(FlexibleModel):
    """
    Issues event configuration.

    Runs your workflow anytime the issues event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#issues-event-issues
    """

    types: list[IssuesActivityType] | IssuesActivityType | None = None


class LabelEvent(FlexibleModel):
    """
    Label event configuration.

    Runs your workflow anytime the label event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#label-event-label
    """

    types: list[LabelActivityType] | LabelActivityType | None = None


class MergeGroupEvent(FlexibleModel):
    """
    Merge group event configuration.

    Runs your workflow when a pull request is added to a merge queue.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#merge_group
    """

    types: list[MergeGroupActivityType] | MergeGroupActivityType | None = None


class MilestoneEvent(FlexibleModel):
    """
    Milestone event configuration.

    Runs your workflow anytime the milestone event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#milestone-event-milestone
    """

    types: list[MilestoneActivityType] | MilestoneActivityType | None = None


class ProjectEvent(FlexibleModel):
    """
    Project event configuration.

    Runs your workflow anytime the project event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#project-event-project
    """

    types: list[ProjectActivityType] | ProjectActivityType | None = None


class ProjectCardEvent(FlexibleModel):
    """
    Project card event configuration.

    Runs your workflow anytime the project_card event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#project-card-event-project_card
    """

    types: list[ProjectCardActivityType] | ProjectCardActivityType | None = None


class ProjectColumnEvent(FlexibleModel):
    """
    Project column event configuration.

    Runs your workflow anytime the project_column event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#project-column-event-project_column
    """

    types: list[ProjectColumnActivityType] | ProjectColumnActivityType | None = None


class PullRequestEvent(StrictModel):
    """
    Pull request event configuration.

    Runs your workflow anytime the pull_request event occurs.

    Note: Workflows do not run on private base repositories when you open a
    pull request from a forked repository.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#pull-request-event-pull_request
    """

    types: list[PullRequestActivityType] | PullRequestActivityType | None = None
    branches: Globs | None = Field(
        default=None,
        description="Filter to specific branches. Cannot be used with branches-ignore.",
    )
    branches_ignore: Globs | None = Field(
        default=None,
        alias="branches-ignore",
        description="Branches to ignore. Cannot be used with branches.",
    )
    tags: Globs | None = Field(
        default=None,
        description="Filter to specific tags. Cannot be used with tags-ignore.",
    )
    tags_ignore: Globs | None = Field(
        default=None,
        alias="tags-ignore",
        description="Tags to ignore. Cannot be used with tags.",
    )
    paths: Globs | None = Field(
        default=None,
        description="Filter to specific paths. Cannot be used with paths-ignore.",
    )
    paths_ignore: Globs | None = Field(
        default=None,
        alias="paths-ignore",
        description="Paths to ignore. Cannot be used with paths.",
    )

    @model_validator(mode="after")
    def check_filter_exclusivity(self) -> PullRequestEvent:
        if self.branches is not None and self.branches_ignore is not None:
            raise ValueError("Cannot use both 'branches' and 'branches-ignore'")
        if self.tags is not None and self.tags_ignore is not None:
            raise ValueError("Cannot use both 'tags' and 'tags-ignore'")
        if self.paths is not None and self.paths_ignore is not None:
            raise ValueError("Cannot use both 'paths' and 'paths-ignore'")
        return self


class PullRequestTargetEvent(StrictModel):
    """
    Pull request target event configuration.

    This event is similar to pull_request, except that it runs in the context
    of the base repository of the pull request, rather than in the merge commit.

    Reference: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#pull_request_target
    """

    types: (
        list[PullRequestTargetActivityType] | PullRequestTargetActivityType | None
    ) = None
    branches: Globs | None = None
    branches_ignore: Globs | None = Field(default=None, alias="branches-ignore")
    tags: Globs | None = None
    tags_ignore: Globs | None = Field(default=None, alias="tags-ignore")
    paths: Globs | None = None
    paths_ignore: Globs | None = Field(default=None, alias="paths-ignore")

    @model_validator(mode="after")
    def check_filter_exclusivity(self) -> PullRequestTargetEvent:
        if self.branches is not None and self.branches_ignore is not None:
            raise ValueError("Cannot use both 'branches' and 'branches-ignore'")
        if self.tags is not None and self.tags_ignore is not None:
            raise ValueError("Cannot use both 'tags' and 'tags-ignore'")
        if self.paths is not None and self.paths_ignore is not None:
            raise ValueError("Cannot use both 'paths' and 'paths-ignore'")
        return self


class PullRequestReviewEvent(FlexibleModel):
    """
    Pull request review event configuration.

    Runs your workflow anytime the pull_request_review event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#pull-request-review-event-pull_request_review
    """

    types: (
        list[PullRequestReviewActivityType] | PullRequestReviewActivityType | None
    ) = None


class PullRequestReviewCommentEvent(FlexibleModel):
    """
    Pull request review comment event configuration.

    Runs your workflow anytime a comment on a pull request's unified diff is modified.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#pull-request-review-comment-event-pull_request_review_comment
    """

    types: (
        list[PullRequestReviewCommentActivityType]
        | PullRequestReviewCommentActivityType
        | None
    ) = None


class PushEvent(StrictModel):
    """
    Push event configuration.

    Runs your workflow when someone pushes to a repository branch.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#push-event-push
    """

    branches: Globs | None = None
    branches_ignore: Globs | None = Field(default=None, alias="branches-ignore")
    tags: Globs | None = None
    tags_ignore: Globs | None = Field(default=None, alias="tags-ignore")
    paths: Globs | None = None
    paths_ignore: Globs | None = Field(default=None, alias="paths-ignore")

    @model_validator(mode="after")
    def check_filter_exclusivity(self) -> PushEvent:
        if self.branches is not None and self.branches_ignore is not None:
            raise ValueError("Cannot use both 'branches' and 'branches-ignore'")
        if self.tags is not None and self.tags_ignore is not None:
            raise ValueError("Cannot use both 'tags' and 'tags-ignore'")
        if self.paths is not None and self.paths_ignore is not None:
            raise ValueError("Cannot use both 'paths' and 'paths-ignore'")
        return self


class RegistryPackageEvent(FlexibleModel):
    """
    Registry package event configuration.

    Runs your workflow anytime a package is published or updated.

    Reference: https://help.github.com/en/actions/reference/events-that-trigger-workflows#registry-package-event-registry_package
    """

    types: list[RegistryPackageActivityType] | RegistryPackageActivityType | None = None


class ReleaseEvent(FlexibleModel):
    """
    Release event configuration.

    Runs your workflow anytime the release event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#release-event-release
    """

    types: list[ReleaseActivityType] | ReleaseActivityType | None = None


class ScheduleItem(StrictModel):
    """A single schedule entry with cron syntax."""

    cron: str = Field(
        ...,
        description="POSIX cron syntax for scheduling. The shortest interval is once every 5 minutes.",
    )


class WorkflowCallEvent(BaseModel):
    """
    Workflow call event configuration.

    Allows workflows to be reused by other workflows.

    Reference: https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#workflow_call
    """

    inputs: dict[str, WorkflowCallInput] | None = Field(
        default=None,
        description="Inputs that are passed to the called workflow from the caller workflow.",
    )
    outputs: dict[str, WorkflowCallOutput] | None = Field(
        default=None,
        description="Outputs that are passed from the called workflow to the caller workflow.",
    )
    secrets: dict[str, WorkflowCallSecret] | None = Field(
        default=None,
        description="A map of the secrets that can be used in the called workflow.",
    )


class WorkflowDispatchEvent(StrictModel):
    """
    Workflow dispatch event configuration.

    You can now create workflows that are manually triggered with the new
    workflow_dispatch event. You will then see a 'Run workflow' button on
    the Actions tab, enabling you to easily trigger a run.

    Reference: https://github.blog/changelog/2020-07-06-github-actions-manual-triggers-with-workflow_dispatch/
    """

    inputs: dict[str, WorkflowDispatchInput] | None = Field(
        default=None,
        description=(
            "Input parameters allow you to specify data that the action expects to use during runtime. "
            "GitHub stores input parameters as environment variables. Input ids with uppercase letters "
            "are converted to lowercase during runtime. We recommend using lowercase input ids."
        ),
    )


class WorkflowRunEvent(FlexibleModel):
    """
    Workflow run event configuration.

    This event occurs when a workflow run is requested or completed, and allows
    you to execute a workflow based on the finished result of another workflow.

    Reference: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#workflow_run
    """

    types: list[WorkflowRunActivityType] | WorkflowRunActivityType | None = None
    workflows: Annotated[list[str], Field(min_length=1)] | None = Field(
        default=None,
        description="The workflows to trigger on.",
    )
    branches: Globs | None = None
    branches_ignore: Globs | None = Field(default=None, alias="branches-ignore")


# =============================================================================
# On (Triggers) Configuration
# =============================================================================


class OnConfiguration(StrictModel):
    """
    Complete event trigger configuration.

    The name of the GitHub event that triggers the workflow. You can provide
    a single event string, array of events, array of event types, or an event
    configuration map that schedules a workflow or restricts the execution of
    a workflow to specific files, tags, or branch changes.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows
    """

    branch_protection_rule: BranchProtectionRuleEvent | None = None
    check_run: CheckRunEvent | None = None
    check_suite: CheckSuiteEvent | None = None
    create: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime someone creates a branch or tag.",
    )
    delete: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime someone deletes a branch or tag.",
    )
    deployment: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime someone creates a deployment.",
    )
    deployment_status: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime a third party provides a deployment status.",
    )
    discussion: DiscussionEvent | None = None
    discussion_comment: DiscussionCommentEvent | None = None
    fork: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime when someone forks a repository.",
    )
    gollum: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow when someone creates or updates a Wiki page.",
    )
    issue_comment: IssueCommentEvent | None = None
    issues: IssuesEvent | None = None
    label: LabelEvent | None = None
    merge_group: MergeGroupEvent | None = None
    milestone: MilestoneEvent | None = None
    page_build: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime someone pushes to a GitHub Pages-enabled branch.",
    )
    project: ProjectEvent | None = None
    project_card: ProjectCardEvent | None = None
    project_column: ProjectColumnEvent | None = None
    public: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime someone makes a private repository public.",
    )
    pull_request: PullRequestEvent | None = None
    pull_request_review: PullRequestReviewEvent | None = None
    pull_request_review_comment: PullRequestReviewCommentEvent | None = None
    pull_request_target: PullRequestTargetEvent | None = None
    push: PushEvent | None = None
    registry_package: RegistryPackageEvent | None = None
    release: ReleaseEvent | None = None
    status: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime the status of a Git commit changes.",
    )
    watch: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime the watch event occurs.",
    )
    workflow_call: WorkflowCallEvent | None = None
    workflow_dispatch: WorkflowDispatchEvent | None = None
    workflow_run: WorkflowRunEvent | None = None
    repository_dispatch: FlexibleModel | None = Field(
        default=None,
        description=(
            "You can use the GitHub API to trigger a webhook event called repository_dispatch "
            "when you want to trigger a workflow for activity that happens outside of GitHub."
        ),
    )
    schedule: Annotated[list[ScheduleItem], Field(min_length=1)] | None = Field(
        default=None,
        description=(
            "You can schedule a workflow to run at specific UTC times using POSIX cron syntax. "
            "The shortest interval you can run scheduled workflows is once every 5 minutes."
        ),
    )


On = EventType | list[EventType] | OnConfiguration
"""
Workflow trigger configuration.

Can be a single event, list of events, or detailed event configuration.
"""


# =============================================================================
# Workflow (Root Model)
# =============================================================================


class Workflow(StrictModel):
    """
    GitHub Actions Workflow definition.

    A workflow is a configurable automated process made up of one or more jobs.
    You must create a YAML file to define your workflow configuration.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions
    """

    name: str | None = Field(
        default=None,
        description=(
            "The name of your workflow. GitHub displays the names of your workflows "
            "on your repository's actions page. If you omit this field, GitHub sets "
            "the name to the workflow's filename."
        ),
    )
    run_name: str | None = Field(
        default=None,
        alias="run-name",
        description=(
            "The name for workflow runs generated from the workflow. GitHub displays "
            "the workflow run name in the list of workflow runs on your repository's 'Actions' tab."
        ),
    )
    on: On = Field(
        ...,
        description=(
            "The name of the GitHub event that triggers the workflow. You can provide "
            "a single event string, array of events, array of event types, or an event "
            "configuration map that schedules a workflow or restricts the execution of "
            "a workflow to specific files, tags, or branch changes."
        ),
    )
    env: EnvMapping | None = Field(
        default=None,
        description="A map of environment variables that are available to all jobs and steps in the workflow.",
    )
    defaults: Defaults | None = Field(
        default=None,
        description="A map of default settings that will apply to all jobs in the workflow.",
    )
    concurrency: str | Concurrency | None = Field(
        default=None,
        description=(
            "Concurrency ensures that only a single job or workflow using the same "
            "concurrency group will run at a time."
        ),
    )
    jobs: Annotated[dict[str, Job], Field(min_length=1)] = Field(
        ...,
        description=(
            "A workflow run is made up of one or more jobs. Jobs run in parallel by default. "
            "To run jobs sequentially, you can define dependencies on other jobs using the "
            "jobs.<job_id>.needs keyword."
        ),
    )
    permissions: Permissions | None = Field(
        default=None,
        description=(
            "You can modify the default permissions granted to the GITHUB_TOKEN, "
            "adding or removing access as required."
        ),
    )

    @field_validator("jobs")
    @classmethod
    def validate_job_ids(cls, v: dict[str, Job]) -> dict[str, Job]:
        """Validate that job IDs match the required pattern."""
        import re

        pattern = re.compile(r"^[_a-zA-Z][a-zA-Z0-9_-]*$")
        for job_id in v:
            if not pattern.match(job_id):
                raise ValueError(
                    f"Invalid job ID '{job_id}': must start with a letter or underscore "
                    "and contain only alphanumeric characters, dashes, or underscores"
                )
        return v


# =============================================================================
# Convenience function for parsing
# =============================================================================


def parse_workflow(data: dict[str, Any]) -> Workflow:
    """
    Parse a workflow dictionary into a Workflow model.

    Args:
        data: Dictionary representation of a GitHub Actions workflow

    Returns:
        Validated Workflow instance

    Raises:
        pydantic.ValidationError: If the workflow data is invalid
    """
    return Workflow.model_validate(data)


def parse_workflow_yaml(yaml_content: str) -> Workflow:
    """
    Parse a YAML string into a Workflow model.

    Args:
        yaml_content: YAML string representation of a GitHub Actions workflow

    Returns:
        Validated Workflow instance

    Raises:
        pydantic.ValidationError: If the workflow data is invalid
        yaml.YAMLError: If the YAML is malformed

    Note:
        Requires PyYAML to be installed.
        Handles the YAML 1.1 quirk where 'on' is parsed as boolean True.
    """
    import yaml

    data = yaml.safe_load(yaml_content)

    # Handle YAML 1.1 quirk: 'on' key is parsed as boolean True
    # This is a known issue with GitHub Actions workflows
    if isinstance(data, dict) and True in data and "on" not in data:
        data["on"] = data.pop(True)

    return parse_workflow(data)
