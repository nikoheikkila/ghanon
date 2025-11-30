"""Tests for GitHub Actions event configurations."""

import pytest
from assertpy import assert_that
from pydantic import ValidationError

from ghanon.models.workflow import (
    BranchProtectionRuleEvent,
    CheckRunEvent,
    CheckSuiteEvent,
    DiscussionCommentEvent,
    DiscussionEvent,
    IssueCommentEvent,
    IssuesEvent,
    LabelEvent,
    MergeGroupEvent,
    MilestoneEvent,
    OnConfiguration,
    ProjectCardEvent,
    ProjectColumnEvent,
    ProjectEvent,
    PullRequestActivityType,
    PullRequestEvent,
    PullRequestReviewCommentEvent,
    PullRequestReviewEvent,
    PullRequestTargetEvent,
    PushEvent,
    RegistryPackageEvent,
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


class TestPushEvent:
    """Tests for push event configuration."""

    def test_empty(self):
        e = PushEvent.model_validate({})
        assert_that(e.branches).is_none()

    def test_branches(self):
        e = PushEvent.model_validate({"branches": ["main", "develop"]})
        assert_that(e.branches).is_equal_to(["main", "develop"])

    def test_branches_ignore(self):
        e = PushEvent.model_validate({"branches-ignore": ["feature/*"]})
        assert_that(e.branches_ignore).is_equal_to(["feature/*"])

    def test_branches_exclusive(self):
        assert_that(PushEvent.model_validate).raises(ValidationError).when_called_with(
            {"branches": ["main"], "branches-ignore": ["dev"]},
        )

    def test_tags(self):
        e = PushEvent.model_validate({"tags": ["v*"]})
        assert_that(e.tags).is_equal_to(["v*"])

    def test_tags_ignore(self):
        e = PushEvent.model_validate({"tags-ignore": ["v0.*"]})
        assert_that(e.tags_ignore).is_equal_to(["v0.*"])

    def test_tags_exclusive(self):
        assert_that(PushEvent.model_validate).raises(ValidationError).when_called_with(
            {"tags": ["v*"], "tags-ignore": ["v0.*"]},
        )

    def test_paths(self):
        e = PushEvent.model_validate({"paths": ["src/**", "*.py"]})
        assert_that(e.paths).is_equal_to(["src/**", "*.py"])

    def test_paths_ignore(self):
        e = PushEvent.model_validate({"paths-ignore": ["docs/**", "*.md"]})
        assert_that(e.paths_ignore).is_equal_to(["docs/**", "*.md"])

    def test_paths_exclusive(self):
        assert_that(PushEvent.model_validate).raises(ValidationError).when_called_with(
            {"paths": ["src/**"], "paths-ignore": ["test/**"]},
        )


class TestPullRequestEvent:
    """Tests for pull_request event configuration."""

    def test_types(self):
        e = PullRequestEvent.model_validate({"types": ["opened", "synchronize", "reopened"]})
        assert_that(e.types).is_length(3)
        assert_that(e.types).contains(PullRequestActivityType.OPENED)

    def test_all_filters(self):
        e = PullRequestEvent.model_validate(
            {
                "types": ["opened"],
                "branches": ["main"],
                "paths": ["src/**"],
            },
        )
        assert_that(e.types).is_equal_to([PullRequestActivityType.OPENED])
        assert_that(e.branches).is_equal_to(["main"])
        assert_that(e.paths).is_equal_to(["src/**"])


class TestPullRequestTargetEvent:
    """Tests for pull_request_target event configuration."""

    def test_types(self):
        e = PullRequestTargetEvent.model_validate({"types": ["opened", "labeled"]})
        assert_that(e.types).is_length(2)

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
        item = ScheduleItem.model_validate({"cron": "0 0 * * *"})
        assert_that(item.cron).is_equal_to("0 0 * * *")

    def test_in_workflow(self, minimal_job):
        w = parse_workflow(
            {
                "on": {"schedule": [{"cron": "0 0 * * *"}, {"cron": "0 12 * * 1-5"}]},
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.on.schedule).is_length(2)


class TestWorkflowDispatchEvent:
    """Tests for workflow_dispatch event configuration."""

    def test_empty(self):
        e = WorkflowDispatchEvent.model_validate({})
        assert_that(e.inputs).is_none()

    def test_string_input(self):
        e = WorkflowDispatchEvent.model_validate(
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
        assert_that(e.inputs["name"].type).is_equal_to(WorkflowDispatchInputType.STRING)

    def test_boolean_input(self):
        e = WorkflowDispatchEvent.model_validate(
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
        assert_that(e.inputs["debug"].type).is_equal_to(WorkflowDispatchInputType.BOOLEAN)

    def test_choice_input(self):
        e = WorkflowDispatchEvent.model_validate(
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
        assert_that(e.inputs["env"].options).is_equal_to(["dev", "staging", "prod"])

    def test_choice_requires_options(self):
        assert_that(WorkflowDispatchInput.model_validate).raises(ValidationError).when_called_with(
            {
                "description": "Env",
                "type": "choice",
            },
        )

    def test_required_input(self):
        e = WorkflowDispatchEvent.model_validate(
            {
                "inputs": {"token": {"description": "API Token", "required": True}},
            },
        )
        assert_that(e.inputs["token"].required).is_true()


class TestWorkflowCallEvent:
    """Tests for workflow_call event configuration."""

    def test_inputs(self):
        e = WorkflowCallEvent.model_validate(
            {
                "inputs": {
                    "environment": {"type": "string", "required": True},
                    "debug": {"type": "boolean", "default": False},
                },
            },
        )
        assert_that(e.inputs["environment"].type).is_equal_to(WorkflowCallInputType.STRING)
        assert_that(e.inputs["debug"].default).is_false()

    def test_outputs(self):
        e = WorkflowCallEvent.model_validate(
            {
                "outputs": {
                    "version": {
                        "description": "The version",
                        "value": "${{ jobs.build.outputs.version }}",
                    },
                },
            },
        )
        assert_that(e.outputs).contains_key("version")

    def test_secrets(self):
        e = WorkflowCallEvent.model_validate(
            {
                "secrets": {
                    "API_KEY": {"description": "API key", "required": True},
                },
            },
        )
        assert_that(e.secrets["API_KEY"].required).is_true()


class TestWorkflowRunEvent:
    """Tests for workflow_run event configuration."""

    def test_types(self):
        e = WorkflowRunEvent.model_validate(
            {
                "types": ["completed"],
                "workflows": ["CI"],
            },
        )
        assert_that(e.types).contains(WorkflowRunActivityType.COMPLETED)

    def test_branches(self):
        e = WorkflowRunEvent.model_validate(
            {
                "workflows": ["Build"],
                "branches": ["main"],
            },
        )
        assert_that(e.branches).is_equal_to(["main"])


class TestActivityTypeEvents:
    """Tests for events with activity types."""

    @pytest.mark.parametrize(
        ("event_class", "types"),
        [
            (BranchProtectionRuleEvent, ["created", "edited", "deleted"]),
            (CheckRunEvent, ["created", "rerequested", "completed"]),
            (CheckSuiteEvent, ["completed", "requested"]),
            (DiscussionEvent, ["created", "answered"]),
            (DiscussionCommentEvent, ["created", "edited"]),
            (IssueCommentEvent, ["created", "deleted"]),
            (IssuesEvent, ["opened", "closed", "labeled"]),
            (LabelEvent, ["created", "deleted"]),
            (MergeGroupEvent, ["checks_requested"]),
            (MilestoneEvent, ["created", "closed"]),
            (ProjectEvent, ["created", "closed"]),
            (ProjectCardEvent, ["created", "moved"]),
            (ProjectColumnEvent, ["created", "moved"]),
            (PullRequestReviewEvent, ["submitted", "dismissed"]),
            (PullRequestReviewCommentEvent, ["created", "edited"]),
            (RegistryPackageEvent, ["published", "updated"]),
            (ReleaseEvent, ["published", "released"]),
        ],
    )
    def test_activity_types(self, event_class, types):
        e = event_class.model_validate({"types": types})
        assert_that(e.types).is_not_none()
        assert_that(e.types).is_length(len(types))


class TestOnConfiguration:
    """Tests for complete on configuration."""

    def test_multiple_events(self, minimal_job):
        w = parse_workflow(
            {
                "on": {
                    "push": {"branches": ["main"]},
                    "pull_request": {"branches": ["main"]},
                    "workflow_dispatch": {},
                },
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.on).is_instance_of(OnConfiguration)
        assert_that(w.on.push).is_not_none()
        assert_that(w.on.pull_request).is_not_none()
        assert_that(w.on.workflow_dispatch).is_not_none()

    def test_simple_events(self, minimal_job):
        w = parse_workflow(
            {
                "on": {"create": None, "delete": None, "fork": None},
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.on).is_instance_of(OnConfiguration)
