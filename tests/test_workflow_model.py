from typing import Any

import pytest
from assertpy import assert_that
from pydantic import ValidationError

from ghanon.domain.defaults import Defaults, DefaultsRun
from ghanon.domain.matrix import Strategy
from ghanon.domain.workflow import (
    Concurrency,
    EventType,
    OnConfiguration,
    PermissionAccess,
    PermissionLevel,
    PermissionsEvent,
    PullRequestEvent,
    PushEvent,
    WorkflowDispatchEvent,
)
from ghanon.parser import parse_workflow


class TestWorkflow:
    def test_minimal(self, minimal_workflow):
        workflow = parse_workflow(minimal_workflow)
        assert_that(workflow.on).is_equal_to(EventType.PUSH)
        assert_that(workflow.jobs).contains_key("build")

    def test_with_name(self, minimal_job):
        workflow = parse_workflow({"name": "CI", "on": "push", "jobs": {"build": minimal_job}})
        assert_that(workflow.name).is_equal_to("CI")

    def test_with_run_name(self, minimal_job):
        run_name = "Deploy by @${{ github.actor }}"

        workflow = parse_workflow(
            {
                "name": "Deploy",
                "run-name": run_name,
                "on": "push",
                "jobs": {"build": minimal_job},
            },
        )

        assert_that(workflow.run_name).is_equal_to(run_name)

    def test_event_list(self, minimal_job):
        events = [EventType.PUSH, EventType.PULL_REQUEST]
        workflow = parse_workflow({"on": events, "jobs": {"build": minimal_job}})
        assert_that(workflow.on).is_equal_to(events)

    def test_env(self, minimal_job):
        env = {"CI": "true", "NODE_VERSION": 18}

        workflow = parse_workflow(
            {
                "on": "push",
                "env": env,
                "jobs": {"build": minimal_job},
            },
        )

        assert_that(workflow.env).is_equal_to(env)

    def test_defaults(self, minimal_job):
        shell = "bash"
        working_directory = "./src"

        workflow = parse_workflow(
            {
                "on": "push",
                "defaults": {"run": {"shell": shell, "working-directory": working_directory}},
                "jobs": {"build": minimal_job},
            },
        )

        assert isinstance(workflow.defaults, Defaults)
        assert isinstance(workflow.defaults.run, DefaultsRun)
        assert_that(workflow.defaults.run.shell).is_equal_to(shell)
        assert_that(workflow.defaults.run.working_directory).is_equal_to(working_directory)

    def test_concurrency_string(self, minimal_job):
        group = "ci-${{ github.ref }}"

        workflow = parse_workflow(
            {
                "on": "push",
                "concurrency": group,
                "jobs": {"build": minimal_job},
            },
        )

        assert_that(workflow.concurrency).is_equal_to(group)

    def test_concurrency_object(self, minimal_job):
        workflow = parse_workflow(
            {
                "on": "push",
                "concurrency": {
                    "group": "ci-${{ github.ref }}",
                    "cancel-in-progress": True,
                },
                "jobs": {"build": minimal_job},
            },
        )

        assert isinstance(workflow.concurrency, Concurrency)
        assert_that(workflow.concurrency.cancel_in_progress).is_true()

    def test_permissions_global(self, minimal_job):
        workflow = parse_workflow(
            {
                "on": "push",
                "permissions": PermissionAccess.READ_ALL,
                "jobs": {
                    "build": minimal_job,
                },
            },
        )

        assert_that(workflow.permissions).is_equal_to(PermissionAccess.READ_ALL)

    def test_permissions_granular(self, minimal_job):
        workflow = parse_workflow(
            {
                "on": "push",
                "permissions": {
                    "contents": PermissionLevel.READ,
                    "pull-requests": PermissionLevel.WRITE,
                    "issues": PermissionLevel.NONE,
                },
                "jobs": {"build": minimal_job},
            },
        )

        assert isinstance(workflow.permissions, PermissionsEvent)
        assert_that(workflow.permissions.contents).is_equal_to(PermissionLevel.READ)
        assert_that(workflow.permissions.pull_requests).is_equal_to(PermissionLevel.WRITE)
        assert_that(workflow.permissions.issues).is_equal_to(PermissionLevel.NONE)

    def test_missing_on_fails(self, minimal_job):
        assert_that(parse_workflow).raises(ValidationError).when_called_with({"jobs": {"build": minimal_job}})

    def test_missing_jobs_fails(self):
        assert_that(parse_workflow).raises(ValidationError).when_called_with({"on": "push"})

    def test_empty_jobs_fails(self):
        assert_that(parse_workflow).raises(ValidationError).when_called_with({"on": "push", "jobs": {}})

    def test_expression_in_env(self, minimal_job: dict):
        env = "${{ fromJson(needs.setup.outputs.env) }}"

        workflow = parse_workflow(
            {
                "on": "push",
                "env": env,
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(workflow.env).is_equal_to(env)

    def test_special_characters_in_name(self, minimal_job: dict):
        workflow = parse_workflow(
            {
                "name": "CI: Build & Test (v2.0)",
                "on": "push",
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(workflow.name).contains("&")

    @pytest.mark.parametrize("invalid_id", ["123start", "-invalid", "has space", "has.dot"])
    def test_invalid_job_id_fails(self, invalid_id, minimal_job):
        assert_that(parse_workflow).raises(ValidationError).when_called_with(
            {"on": "push", "jobs": {invalid_id: minimal_job}},
        )

    @pytest.mark.parametrize("valid_id", ["build", "_private", "test_job", "job-1", "A1"])
    def test_valid_job_ids(self, valid_id, minimal_job):
        w = parse_workflow({"on": "push", "jobs": {valid_id: minimal_job}})
        assert_that(w.jobs).contains_key(valid_id)


class TestOnConfiguration:
    def test_multiple_events(self, minimal_job: dict[str, Any]):
        branches = ["main"]
        triggers = {"branches": branches}

        workflow = parse_workflow(
            {
                "on": {
                    "push": triggers,
                    "pull_request": triggers,
                    "workflow_dispatch": {},
                },
                "jobs": {"build": minimal_job},
            },
        )

        assert isinstance(workflow.on, OnConfiguration)
        assert isinstance(workflow.on.push, PushEvent)
        assert isinstance(workflow.on.pull_request, PullRequestEvent)
        assert isinstance(workflow.on.workflow_dispatch, WorkflowDispatchEvent)
        assert_that(workflow.on.push.branches).is_equal_to(branches)
        assert_that(workflow.on.pull_request.branches).is_equal_to(branches)

    def test_simple_events(self, minimal_job: dict[str, Any]):
        workflow = parse_workflow(
            {
                "on": {"create": None, "delete": None, "fork": None},
                "jobs": {"build": minimal_job},
            },
        )

        assert isinstance(workflow.on, OnConfiguration)
        assert_that(workflow.on.create).is_none()
        assert_that(workflow.on.delete).is_none()
        assert_that(workflow.on.fork).is_none()


class TestRoundTrip:
    def test_workflow_to_dict(self, minimal_workflow):
        workflow = parse_workflow(minimal_workflow)
        dump = workflow.model_dump_json()
        assert_that(dump).snapshot("test_workflow_to_dict")

    def test_workflow_round_trip(self, minimal_workflow):
        first_workflow = parse_workflow(minimal_workflow)
        dump = first_workflow.model_dump(by_alias=True, exclude_none=True)
        second_workflow = parse_workflow(dump)

        assert_that(first_workflow.on).is_equal_to(second_workflow.on)
        assert_that(list(first_workflow.jobs.keys())).is_equal_to(list(second_workflow.jobs.keys()))

    def test_complex_round_trip(self):
        data = {
            "name": "Test",
            "on": {"push": {"branches": ["main"]}, "pull_request": {}},
            "concurrency": {"group": "ci", "cancel-in-progress": True},
            "jobs": {
                "build": {
                    "runs-on": "ubuntu-latest",
                    "strategy": {"matrix": {"node": ["18", "20"]}},
                    "steps": [
                        {"uses": "actions/checkout@v4"},
                        {"run": "npm test", "shell": "bash"},
                    ],
                },
            },
        }

        first_workflow = parse_workflow(data)
        dump = first_workflow.model_dump(by_alias=True, exclude_none=True)
        second_workflow = parse_workflow(dump)
        first_build_job = first_workflow.jobs["build"]
        second_build_job = second_workflow.jobs["build"]

        assert isinstance(first_build_job.strategy, Strategy)
        assert isinstance(second_build_job.strategy, Strategy)
        assert_that(first_workflow.on).is_equal_to(second_workflow.on)
        assert_that(first_build_job).is_equal_to(second_build_job)
