"""Enumerations for GitHub Actions workflow models."""

from __future__ import annotations

from enum import Enum, StrEnum

__all__ = [
    "Architecture",
    "BranchProtectionRuleActivityType",
    "CheckRunActivityType",
    "CheckSuiteActivityType",
    "DiscussionActivityType",
    "DiscussionCommentActivityType",
    "EventType",
    "IssueCommentActivityType",
    "IssuesActivityType",
    "LabelActivityType",
    "Machine",
    "MergeGroupActivityType",
    "MilestoneActivityType",
    "ModelPermissionLevel",
    "PermissionAccess",
    "PermissionLevel",
    "ProjectActivityType",
    "ProjectCardActivityType",
    "ProjectColumnActivityType",
    "PullRequestActivityType",
    "PullRequestReviewActivityType",
    "PullRequestReviewCommentActivityType",
    "PullRequestTargetActivityType",
    "RegistryPackageActivityType",
    "ReleaseActivityType",
    "ShellType",
    "WorkflowCallInputType",
    "WorkflowDispatchInputType",
    "WorkflowRunActivityType",
]


class PermissionLevel(str, Enum):
    """Permission access levels for GITHUB_TOKEN."""

    READ = "read"
    WRITE = "write"
    NONE = "none"


class PermissionAccess(str, Enum):
    """Global permission access shortcuts."""

    READ_ALL = "read-all"
    WRITE_ALL = "write-all"


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


class ModelPermissionLevel(str, Enum):
    """Permission levels for models (restricted to read/none)."""

    READ = "read"
    NONE = "none"


class ShellType(StrEnum):
    """Built-in shell types."""

    BASH = "bash"
    PWSH = "pwsh"
    PYTHON = "python"
    SH = "sh"
    CMD = "cmd"
    POWERSHELL = "powershell"


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
