import pytest
from assertpy import assert_that

from ghanon.models.workflow import (
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
    PullRequestReviewActivityType,
    PullRequestReviewCommentActivityType,
    PullRequestReviewCommentEvent,
    PullRequestReviewEvent,
    RegistryPackageActivityType,
    RegistryPackageEvent,
    ReleaseActivityType,
    ReleaseEvent,
    WorkflowCallEvent,
    WorkflowCallInputType,
    WorkflowRunActivityType,
    WorkflowRunEvent,
)


class TestWorkflowCallEvent:
    def test_inputs(self):
        event = WorkflowCallEvent.model_validate(
            {
                "inputs": {
                    "environment": {"type": "string", "required": True},
                    "debug": {"type": "boolean", "default": False},
                },
            },
        )

        assert event.inputs is not None
        assert_that(event.inputs["environment"].type).is_equal_to(WorkflowCallInputType.STRING)
        assert_that(event.inputs["debug"].default).is_false()

    def test_outputs(self):
        event = WorkflowCallEvent.model_validate(
            {
                "outputs": {
                    "version": {
                        "description": "v1.2.3",
                        "value": "${{ jobs.build.outputs.version }}",
                    },
                },
            },
        )

        assert event.outputs is not None
        assert_that(event.outputs["version"].description).is_equal_to("v1.2.3")
        assert_that(event.outputs["version"].value).is_equal_to("${{ jobs.build.outputs.version }}")

    def test_secrets(self):
        event = WorkflowCallEvent.model_validate(
            {
                "secrets": {
                    "API_KEY": {"description": "API key", "required": True},
                },
            },
        )

        assert event.secrets is not None
        assert_that(event.secrets["API_KEY"].required).is_true()
        assert_that(event.secrets["API_KEY"].description).is_equal_to("API key")


class TestWorkflowRunEvent:
    def test_types(self):
        event = WorkflowRunEvent.model_validate(
            {
                "types": [WorkflowRunActivityType.COMPLETED],
                "workflows": ["CI"],
            },
        )

        assert_that(event.types).contains(WorkflowRunActivityType.COMPLETED)
        assert_that(event.workflows).contains("CI")

    def test_branches(self):
        event = WorkflowRunEvent.model_validate(
            {
                "workflows": ["Build"],
                "branches": ["main"],
            },
        )

        assert_that(event.branches).is_equal_to(["main"])
        assert_that(event.workflows).contains("Build")


class TestActivityTypeEvents:
    @pytest.mark.parametrize(
        ("event_class", "types"),
        [
            (
                BranchProtectionRuleEvent,
                [
                    BranchProtectionRuleActivityType.CREATED,
                    BranchProtectionRuleActivityType.EDITED,
                    BranchProtectionRuleActivityType.DELETED,
                ],
            ),
            (
                CheckRunEvent,
                [
                    CheckRunActivityType.CREATED,
                    CheckRunActivityType.REREQUESTED,
                    CheckRunActivityType.COMPLETED,
                ],
            ),
            (
                CheckSuiteEvent,
                [CheckSuiteActivityType.COMPLETED, CheckSuiteActivityType.REQUESTED],
            ),
            (
                DiscussionEvent,
                [DiscussionActivityType.CREATED, DiscussionActivityType.ANSWERED],
            ),
            (
                DiscussionCommentEvent,
                [DiscussionCommentActivityType.CREATED, DiscussionCommentActivityType.EDITED],
            ),
            (
                IssueCommentEvent,
                [IssueCommentActivityType.CREATED, IssueCommentActivityType.DELETED],
            ),
            (
                IssuesEvent,
                [IssuesActivityType.OPENED, IssuesActivityType.CLOSED, IssuesActivityType.LABELED],
            ),
            (LabelEvent, [LabelActivityType.CREATED, LabelActivityType.DELETED]),
            (MergeGroupEvent, [MergeGroupActivityType.CHECKS_REQUESTED]),
            (
                MilestoneEvent,
                [MilestoneActivityType.CREATED, MilestoneActivityType.CLOSED],
            ),
            (ProjectEvent, [ProjectActivityType.CREATED, ProjectActivityType.CLOSED]),
            (
                ProjectCardEvent,
                [ProjectCardActivityType.CREATED, ProjectCardActivityType.MOVED],
            ),
            (
                ProjectColumnEvent,
                [ProjectColumnActivityType.CREATED, ProjectColumnActivityType.MOVED],
            ),
            (
                PullRequestReviewEvent,
                [
                    PullRequestReviewActivityType.SUBMITTED,
                    PullRequestReviewActivityType.DISMISSED,
                ],
            ),
            (
                PullRequestReviewCommentEvent,
                [
                    PullRequestReviewCommentActivityType.CREATED,
                    PullRequestReviewCommentActivityType.EDITED,
                ],
            ),
            (
                RegistryPackageEvent,
                [RegistryPackageActivityType.PUBLISHED, RegistryPackageActivityType.UPDATED],
            ),
            (
                ReleaseEvent,
                [ReleaseActivityType.PUBLISHED, ReleaseActivityType.RELEASED],
            ),
        ],
    )
    def test_activity_types(self, event_class, types):
        event = event_class.model_validate({"types": types})
        assert_that(event.types).contains(*types)
