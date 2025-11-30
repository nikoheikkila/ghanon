"""Pydantic models for GitHub Actions Workflow schema.

Based on: https://json.schemastore.org/github-workflow.json
Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .concurrency import Concurrency
from .container import Container, ContainerCredentials
from .defaults import Defaults, DefaultsRun, ShellType
from .environment import Environment
from .events import (
    BranchProtectionRuleActivityType,
    BranchProtectionRuleEvent,
    CheckRunActivityType,
    CheckRunEvent,
    CheckSuiteActivityType,
    CheckSuiteEvent,
    DiscussionActivityType,
    DiscussionCommentActivityType,
    DiscussionCommentEvent,
    DiscussionEvent,
    Globs,
    IssueCommentActivityType,
    IssueCommentEvent,
    IssuesActivityType,
    IssuesEvent,
    LabelActivityType,
    LabelEvent,
    MergeGroupActivityType,
    MergeGroupEvent,
    MilestoneActivityType,
    MilestoneEvent,
    ProjectActivityType,
    ProjectCardActivityType,
    ProjectCardEvent,
    ProjectColumnActivityType,
    ProjectColumnEvent,
    ProjectEvent,
    PullRequestActivityType,
    PullRequestEvent,
    PullRequestReviewActivityType,
    PullRequestReviewCommentActivityType,
    PullRequestReviewCommentEvent,
    PullRequestReviewEvent,
    PullRequestTargetActivityType,
    PullRequestTargetEvent,
    PushEvent,
    RegistryPackageActivityType,
    RegistryPackageEvent,
    ReleaseActivityType,
    ReleaseEvent,
    ScheduleItem,
    WorkflowCallEvent,
    WorkflowCallInput,
    WorkflowCallInputType,
    WorkflowCallOutput,
    WorkflowCallSecret,
    WorkflowDispatchEvent,
    WorkflowDispatchInput,
    WorkflowDispatchInputType,
    WorkflowRunActivityType,
    WorkflowRunEvent,
)
from .jobs import (
    Job,
    JobName,
    JobNeeds,
    NormalJob,
    ReusableWorkflowCallJob,
    RunnerGroup,
    RunsOn,
    Step,
)
from .matrix import (
    Configuration,
    Matrix,
    MatrixIncludeExclude,
    Strategy,
)
from .permissions import (
    ModelPermissionLevel,
    PermissionAccess,
    PermissionLevel,
    Permissions,
    PermissionsEvent,
)

__all__ = [
    "Architecture",
    "BranchProtectionRuleActivityType",
    "BranchProtectionRuleEvent",
    "CheckRunActivityType",
    "CheckRunEvent",
    "CheckSuiteActivityType",
    "CheckSuiteEvent",
    "Concurrency",
    "Configuration",
    "Container",
    "ContainerCredentials",
    "Defaults",
    "DefaultsRun",
    "DiscussionActivityType",
    "DiscussionCommentActivityType",
    "DiscussionCommentEvent",
    "DiscussionEvent",
    "EnvMapping",
    "EnvVarValue",
    "Environment",
    "EventType",
    "ExpressionSyntax",
    "Globs",
    "IssueCommentActivityType",
    "IssueCommentEvent",
    "IssuesActivityType",
    "IssuesEvent",
    "Job",
    "JobName",
    "JobNeeds",
    "LabelActivityType",
    "LabelEvent",
    "Machine",
    "Matrix",
    "MatrixIncludeExclude",
    "MergeGroupActivityType",
    "MergeGroupEvent",
    "MilestoneActivityType",
    "MilestoneEvent",
    "ModelPermissionLevel",
    "NormalJob",
    "On",
    "OnConfiguration",
    "PermissionAccess",
    "PermissionLevel",
    "Permissions",
    "PermissionsEvent",
    "ProjectActivityType",
    "ProjectCardActivityType",
    "ProjectCardEvent",
    "ProjectColumnActivityType",
    "ProjectColumnEvent",
    "ProjectEvent",
    "PullRequestActivityType",
    "PullRequestEvent",
    "PullRequestReviewActivityType",
    "PullRequestReviewCommentActivityType",
    "PullRequestReviewCommentEvent",
    "PullRequestReviewEvent",
    "PullRequestTargetActivityType",
    "PullRequestTargetEvent",
    "PushEvent",
    "RegistryPackageActivityType",
    "RegistryPackageEvent",
    "ReleaseActivityType",
    "ReleaseEvent",
    "ReusableWorkflowCallJob",
    "RunnerGroup",
    "RunsOn",
    "ScheduleItem",
    "ShellType",
    "Step",
    "Strategy",
    "StringContainingExpression",
    "Workflow",
    "WorkflowCallEvent",
    "WorkflowCallInput",
    "WorkflowCallInputType",
    "WorkflowCallOutput",
    "WorkflowCallSecret",
    "WorkflowDispatchEvent",
    "WorkflowDispatchInput",
    "WorkflowDispatchInputType",
    "WorkflowRunActivityType",
    "WorkflowRunEvent",
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


class EventType(str, Enum):
    """GitHub events that can trigger workflows.

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
# Type Aliases
# =============================================================================

ExpressionSyntax = Annotated[str, Field(pattern=r"^\$\{\{(.|\r|\n)*\}\}$")]
"""GitHub Actions expression syntax: ${{ ... }}"""

StringContainingExpression = Annotated[str, Field(pattern=r"^.*\$\{\{(.|\r|\n)*\}\}.*$")]
"""String containing GitHub Actions expression syntax."""


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
# On (Triggers) Configuration
# =============================================================================


class OnConfiguration(StrictModel):
    """Complete event trigger configuration.

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
    """GitHub Actions Workflow definition.

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
            "You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required."
        ),
    )

    @field_validator("jobs")
    @classmethod
    def validate_job_ids(cls, v: dict[str, Job]) -> dict[str, Job]:
        """Validate that job IDs match the required pattern."""
        pattern = re.compile(r"^[_a-zA-Z][a-zA-Z0-9_-]*$")
        for job_id in v:
            if not pattern.match(job_id):
                msg = (
                    f"Invalid job ID '{job_id}': must start with a letter or underscore "
                    "and contain only alphanumeric characters, dashes, or underscores"
                )
                raise ValueError(
                    msg,
                )
        return v
