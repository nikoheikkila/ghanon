"""Event configuration models for GitHub Actions Workflows.

Reference: https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows
"""

from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, model_validator

from .base import FlexibleModel, StrictModel

__all__ = [
    "BranchProtectionRuleActivityType",
    "BranchProtectionRuleEvent",
    "CheckRunActivityType",
    "CheckRunEvent",
    "CheckSuiteActivityType",
    "CheckSuiteEvent",
    "DiscussionActivityType",
    "DiscussionCommentActivityType",
    "DiscussionCommentEvent",
    "DiscussionEvent",
    "Globs",
    "IssueCommentActivityType",
    "IssueCommentEvent",
    "IssuesActivityType",
    "IssuesEvent",
    "LabelActivityType",
    "LabelEvent",
    "MergeGroupActivityType",
    "MergeGroupEvent",
    "MilestoneActivityType",
    "MilestoneEvent",
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
    "ScheduleItem",
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
# Type Aliases
# =============================================================================

Globs = Annotated[list[str], Field(min_length=1)]
"""Array of glob patterns with at least one item."""


# =============================================================================
# Activity Type Enums
# =============================================================================


class BranchProtectionRuleActivityType(str, Enum):
    """Activity types for branch_protection_rule events."""

    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class CheckRunActivityType(str, Enum):
    """Activity types for check_run events."""

    CREATED = "created"
    REREQUESTED = "rerequested"
    COMPLETED = "completed"
    REQUESTED_ACTION = "requested_action"


class CheckSuiteActivityType(str, Enum):
    """Activity types for check_suite events."""

    COMPLETED = "completed"
    REQUESTED = "requested"
    REREQUESTED = "rerequested"


class DiscussionActivityType(str, Enum):
    """Activity types for discussion events."""

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
    """Activity types for discussion_comment events."""

    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class IssueCommentActivityType(str, Enum):
    """Activity types for issue_comment events."""

    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class IssuesActivityType(str, Enum):
    """Activity types for issues events."""

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
    """Activity types for label events."""

    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class MergeGroupActivityType(str, Enum):
    """Activity types for merge_group events."""

    CHECKS_REQUESTED = "checks_requested"


class MilestoneActivityType(str, Enum):
    """Activity types for milestone events."""

    CREATED = "created"
    CLOSED = "closed"
    OPENED = "opened"
    EDITED = "edited"
    DELETED = "deleted"


class ProjectActivityType(str, Enum):
    """Activity types for project events."""

    CREATED = "created"
    UPDATED = "updated"
    CLOSED = "closed"
    REOPENED = "reopened"
    EDITED = "edited"
    DELETED = "deleted"


class ProjectCardActivityType(str, Enum):
    """Activity types for project_card events."""

    CREATED = "created"
    MOVED = "moved"
    CONVERTED = "converted"
    EDITED = "edited"
    DELETED = "deleted"


class ProjectColumnActivityType(str, Enum):
    """Activity types for project_column events."""

    CREATED = "created"
    UPDATED = "updated"
    MOVED = "moved"
    DELETED = "deleted"


class PullRequestActivityType(str, Enum):
    """Activity types for pull_request events."""

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
    """Activity types for pull_request_target events."""

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
    """Activity types for pull_request_review events."""

    SUBMITTED = "submitted"
    EDITED = "edited"
    DISMISSED = "dismissed"


class PullRequestReviewCommentActivityType(str, Enum):
    """Activity types for pull_request_review_comment events."""

    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class RegistryPackageActivityType(str, Enum):
    """Activity types for registry_package events."""

    PUBLISHED = "published"
    UPDATED = "updated"


class ReleaseActivityType(str, Enum):
    """Activity types for release events."""

    PUBLISHED = "published"
    UNPUBLISHED = "unpublished"
    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"
    PRERELEASED = "prereleased"
    RELEASED = "released"


class WorkflowRunActivityType(str, Enum):
    """Activity types for workflow_run events."""

    REQUESTED = "requested"
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"


class WorkflowDispatchInputType(str, Enum):
    """Input types for workflow_dispatch events."""

    STRING = "string"
    CHOICE = "choice"
    BOOLEAN = "boolean"
    NUMBER = "number"
    ENVIRONMENT = "environment"


class WorkflowCallInputType(str, Enum):
    """Input types for workflow_call events."""

    BOOLEAN = "boolean"
    NUMBER = "number"
    STRING = "string"


# =============================================================================
# Event Configurations
# =============================================================================


class BranchProtectionRuleEvent(FlexibleModel):
    """Branch protection rule event configuration.

    Runs your workflow anytime the branch_protection_rule event occurs.

    Reference: https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#branch_protection_rule
    """

    types: list[BranchProtectionRuleActivityType] | BranchProtectionRuleActivityType | None = None


class CheckRunEvent(FlexibleModel):
    """Check run event configuration.

    Runs your workflow anytime the check_run event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#check-run-event-check_run
    """

    types: list[CheckRunActivityType] | CheckRunActivityType | None = None


class CheckSuiteEvent(FlexibleModel):
    """Check suite event configuration.

    Runs your workflow anytime the check_suite event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#check-suite-event-check_suite
    """

    types: list[CheckSuiteActivityType] | CheckSuiteActivityType | None = None


class DiscussionEvent(FlexibleModel):
    """Discussion event configuration.

    Runs your workflow anytime the discussion event occurs.

    Reference: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#discussion
    """

    types: list[DiscussionActivityType] | DiscussionActivityType | None = None


class DiscussionCommentEvent(FlexibleModel):
    """Discussion comment event configuration.

    Reference: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#discussion_comment
    """

    types: list[DiscussionCommentActivityType] | DiscussionCommentActivityType | None = None


class IssueCommentEvent(FlexibleModel):
    """Issue comment event configuration.

    Runs your workflow anytime the issue_comment event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#issue-comment-event-issue_comment
    """

    types: list[IssueCommentActivityType] | IssueCommentActivityType | None = None


class IssuesEvent(FlexibleModel):
    """Issues event configuration.

    Runs your workflow anytime the issues event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#issues-event-issues
    """

    types: list[IssuesActivityType] | IssuesActivityType | None = None


class LabelEvent(FlexibleModel):
    """Label event configuration.

    Runs your workflow anytime the label event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#label-event-label
    """

    types: list[LabelActivityType] | LabelActivityType | None = None


class MergeGroupEvent(FlexibleModel):
    """Merge group event configuration.

    Runs your workflow when a pull request is added to a merge queue.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#merge_group
    """

    types: list[MergeGroupActivityType] | MergeGroupActivityType | None = None


class MilestoneEvent(FlexibleModel):
    """Milestone event configuration.

    Runs your workflow anytime the milestone event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#milestone-event-milestone
    """

    types: list[MilestoneActivityType] | MilestoneActivityType | None = None


class ProjectEvent(FlexibleModel):
    """Project event configuration.

    Runs your workflow anytime the project event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#project-event-project
    """

    types: list[ProjectActivityType] | ProjectActivityType | None = None


class ProjectCardEvent(FlexibleModel):
    """Project card event configuration.

    Runs your workflow anytime the project_card event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#project-card-event-project_card
    """

    types: list[ProjectCardActivityType] | ProjectCardActivityType | None = None


class ProjectColumnEvent(FlexibleModel):
    """Project column event configuration.

    Runs your workflow anytime the project_column event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#project-column-event-project_column
    """

    types: list[ProjectColumnActivityType] | ProjectColumnActivityType | None = None


class PullRequestEvent(StrictModel):
    """Pull request event configuration.

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
        """Validate that inclusive and exclusive filters are not used together."""
        if self.branches is not None and self.branches_ignore is not None:
            msg = "Cannot use both 'branches' and 'branches-ignore'"
            raise ValueError(msg)
        if self.tags is not None and self.tags_ignore is not None:
            msg = "Cannot use both 'tags' and 'tags-ignore'"
            raise ValueError(msg)
        if self.paths is not None and self.paths_ignore is not None:
            msg = "Cannot use both 'paths' and 'paths-ignore'"
            raise ValueError(msg)
        return self


class PullRequestTargetEvent(StrictModel):
    """Pull request target event configuration.

    This event is similar to pull_request, except that it runs in the context
    of the base repository of the pull request, rather than in the merge commit.

    Reference: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#pull_request_target
    """

    types: list[PullRequestTargetActivityType] | PullRequestTargetActivityType | None = None
    branches: Globs | None = None
    branches_ignore: Globs | None = Field(default=None, alias="branches-ignore")
    tags: Globs | None = None
    tags_ignore: Globs | None = Field(default=None, alias="tags-ignore")
    paths: Globs | None = None
    paths_ignore: Globs | None = Field(default=None, alias="paths-ignore")

    @model_validator(mode="after")
    def check_filter_exclusivity(self) -> PullRequestTargetEvent:
        """Validate that inclusive and exclusive filters are not used together."""
        if self.branches is not None and self.branches_ignore is not None:
            msg = "Cannot use both 'branches' and 'branches-ignore'"
            raise ValueError(msg)
        if self.tags is not None and self.tags_ignore is not None:
            msg = "Cannot use both 'tags' and 'tags-ignore'"
            raise ValueError(msg)
        if self.paths is not None and self.paths_ignore is not None:
            msg = "Cannot use both 'paths' and 'paths-ignore'"
            raise ValueError(msg)
        return self


class PullRequestReviewEvent(FlexibleModel):
    """Pull request review event configuration.

    Runs your workflow anytime the pull_request_review event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#pull-request-review-event-pull_request_review
    """

    types: list[PullRequestReviewActivityType] | PullRequestReviewActivityType | None = None


class PullRequestReviewCommentEvent(FlexibleModel):
    """Pull request review comment event configuration.

    Runs your workflow anytime a comment on a pull request's unified diff is modified.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#pull-request-review-comment-event-pull_request_review_comment
    """

    types: list[PullRequestReviewCommentActivityType] | PullRequestReviewCommentActivityType | None = None


class PushEvent(StrictModel):
    """Push event configuration.

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
        """Validate that inclusive and exclusive filters are not used together."""
        if self.branches is not None and self.branches_ignore is not None:
            msg = "Cannot use both 'branches' and 'branches-ignore'"
            raise ValueError(msg)
        if self.tags is not None and self.tags_ignore is not None:
            msg = "Cannot use both 'tags' and 'tags-ignore'"
            raise ValueError(msg)
        if self.paths is not None and self.paths_ignore is not None:
            msg = "Cannot use both 'paths' and 'paths-ignore'"
            raise ValueError(msg)
        return self


class RegistryPackageEvent(FlexibleModel):
    """Registry package event configuration.

    Runs your workflow anytime a package is published or updated.

    Reference: https://help.github.com/en/actions/reference/events-that-trigger-workflows#registry-package-event-registry_package
    """

    types: list[RegistryPackageActivityType] | RegistryPackageActivityType | None = None


class ReleaseEvent(FlexibleModel):
    """Release event configuration.

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


class WorkflowDispatchInput(StrictModel):
    """Input parameter for workflow_dispatch event.

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
        """Validate that options are provided when type is choice."""
        if self.type == WorkflowDispatchInputType.CHOICE and self.options is None:
            msg = "'options' is required when type is 'choice'"
            raise ValueError(msg)
        return self


class WorkflowDispatchEvent(StrictModel):
    """Workflow dispatch event configuration.

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


class WorkflowCallEvent(BaseModel):
    """Workflow call event configuration.

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


class WorkflowRunEvent(FlexibleModel):
    """Workflow run event configuration.

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
