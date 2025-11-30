"""Pydantic models for GitHub Actions Workflow schema.

Based on: https://json.schemastore.org/github-workflow.json
Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions
"""

from __future__ import annotations

import re
from typing import Annotated

from pydantic import Field, field_validator

from .base import StrictModel
from .concurrency import Concurrency
from .container import Container, ContainerCredentials
from .defaults import Defaults, DefaultsRun, ShellType
from .enums import Architecture, EventType, Machine
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
    NormalJob,
    ReusableWorkflowCallJob,
    Step,
)
from .matrix import (
    Matrix,
    Strategy,
)
from .permissions import (
    ModelPermissionLevel,
    PermissionAccess,
    PermissionLevel,
    Permissions,
    PermissionsEvent,
)
from .runner import RunnerGroup, RunsOn
from .triggers import On, OnConfiguration
from .types import (
    Configuration,
    EnvMapping,
    EnvVarValue,
    ExpressionSyntax,
    JobName,
    JobNeeds,
    MatrixIncludeExclude,
    StringContainingExpression,
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
