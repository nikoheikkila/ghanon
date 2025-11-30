from typing import Any

import pytest
from assertpy import assert_that
from pydantic import ValidationError

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
    OnConfiguration,
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
    PullRequestTargetEvent,
    RegistryPackageActivityType,
    RegistryPackageEvent,
    ReleaseActivityType,
    ReleaseEvent,
    ScheduleItem,
    WorkflowCallEvent,
    WorkflowCallInputType,
    WorkflowDispatchEvent,
    WorkflowDispatchInput,
    WorkflowDispatchInputType,
    WorkflowRunActivityType,
    WorkflowRunEvent,
)
from ghanon.parser import parse_workflow


class TestPullRequestEvent:
    """Tests for pull_request event configuration."""

    def test_types(self):
        types = [
            PullRequestActivityType.OPENED,
            PullRequestActivityType.SYNCHRONIZE,
            PullRequestActivityType.REOPENED,
        ]
        event = PullRequestEvent.model_validate({"types": types})
        assert_that(event.types).contains(*types)

    def test_all_filters(self):
        event = PullRequestEvent.model_validate(
            {
                "types": [PullRequestActivityType.OPENED],
                "branches": ["main"],
                "paths": ["src/**"],
            },
        )
        assert_that(event.types).is_equal_to([PullRequestActivityType.OPENED])
        assert_that(event.branches).is_equal_to(["main"])
        assert_that(event.paths).is_equal_to(["src/**"])


class TestPullRequestTargetEvent:
    def test_types(self):
        types = [PullRequestActivityType.LABELED, PullRequestActivityType.OPENED]
        event = PullRequestTargetEvent.model_validate({"types": types})
        assert_that(event.types).contains(*types)

    def test_filter_exclusivity(self):
        assert_that(PullRequestTargetEvent.model_validate).raises(ValidationError).when_called_with(
            {
                "branches": ["main"],
                "branches-ignore": ["feature/*"],
            },
        )


class TestScheduleEvent:
    """Tests for schedule event configuration."""

    def test_single_cron(self):
        pattern = "0 0 * * *"
        item = ScheduleItem.model_validate({"cron": pattern})
        assert_that(item.cron).is_equal_to(pattern)

    def test_in_workflow(self, minimal_job: dict[str, Any]):
        patterns = [{"cron": "0 0 * * *"}, {"cron": "0 12 * * 1-5"}]
        workflow = parse_workflow(
            {
                "on": {"schedule": patterns},
                "jobs": {"build": minimal_job},
            },
        )

        assert isinstance(workflow.on, OnConfiguration)
        assert isinstance(workflow.on.schedule, list)
        assert_that(workflow.on.schedule[0].cron).is_equal_to("0 0 * * *")
        assert_that(workflow.on.schedule[1].cron).is_equal_to("0 12 * * 1-5")


class TestWorkflowDispatchEvent:
    def test_empty(self):
        event = WorkflowDispatchEvent.model_validate({})
        assert_that(event.inputs).is_none()

    def test_string_input(self):
        event = WorkflowDispatchEvent.model_validate(
            {
                "inputs": {
                    "name": {
                        "description": "Name",
                        "type": "string",
                        "default": "world",
                    },
                },
            },
        )

        assert event.inputs is not None
        assert_that(event.inputs["name"].type).is_equal_to(WorkflowDispatchInputType.STRING)

    def test_boolean_input(self):
        event = WorkflowDispatchEvent.model_validate(
            {
                "inputs": {
                    "debug": {
                        "description": "Debug",
                        "type": "boolean",
                        "default": False,
                    },
                },
            },
        )

        assert event.inputs is not None
        assert_that(event.inputs["debug"].type).is_equal_to(WorkflowDispatchInputType.BOOLEAN)

    def test_choice_input(self):
        event = WorkflowDispatchEvent.model_validate(
            {
                "inputs": {
                    "env": {
                        "description": "Environment",
                        "type": "choice",
                        "options": ["dev", "staging", "prod"],
                    },
                },
            },
        )

        assert event.inputs is not None
        assert_that(event.inputs["env"].options).is_equal_to(["dev", "staging", "prod"])

    def test_choice_requires_options(self):
        assert_that(WorkflowDispatchInput.model_validate).raises(ValidationError).when_called_with(
            {
                "description": "Env",
                "type": "choice",
            },
        )

    def test_required_input(self):
        event = WorkflowDispatchEvent.model_validate(
            {
                "inputs": {"token": {"description": "API Token", "required": True}},
            },
        )

        assert event.inputs is not None
        assert_that(event.inputs["token"].required).is_true()


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
