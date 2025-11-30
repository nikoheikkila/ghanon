"""Tests for root Workflow model."""

import pytest
from assertpy import assert_that
from pydantic import ValidationError

from ghanon.models.workflow import (
    Concurrency,
    EventType,
    PermissionAccess,
    PermissionLevel,
    PermissionsEvent,
)
from ghanon.parser import parse_workflow


class TestWorkflow:
    """Tests for the root Workflow model."""

    def test_minimal(self, minimal_workflow):
        w = parse_workflow(minimal_workflow)
        assert_that(w.on).is_equal_to(EventType.PUSH)
        assert_that(w.jobs).contains_key("build")

    def test_with_name(self, minimal_job):
        w = parse_workflow({"name": "CI", "on": "push", "jobs": {"build": minimal_job}})
        assert_that(w.name).is_equal_to("CI")

    def test_with_run_name(self, minimal_job):
        w = parse_workflow(
            {
                "name": "Deploy",
                "run-name": "Deploy by @${{ github.actor }}",
                "on": "push",
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.run_name).is_equal_to("Deploy by @${{ github.actor }}")

    def test_event_list(self, minimal_job):
        w = parse_workflow({"on": ["push", "pull_request"], "jobs": {"build": minimal_job}})
        assert_that(w.on).is_equal_to([EventType.PUSH, EventType.PULL_REQUEST])

    def test_env(self, minimal_job):
        w = parse_workflow(
            {
                "on": "push",
                "env": {"CI": "true", "NODE_VERSION": 18},
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.env).is_equal_to({"CI": "true", "NODE_VERSION": 18})

    def test_defaults(self, minimal_job):
        w = parse_workflow(
            {
                "on": "push",
                "defaults": {"run": {"shell": "bash", "working-directory": "./src"}},
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.defaults.run.shell).is_equal_to("bash")
        assert_that(w.defaults.run.working_directory).is_equal_to("./src")

    def test_concurrency_string(self, minimal_job):
        w = parse_workflow(
            {
                "on": "push",
                "concurrency": "ci-${{ github.ref }}",
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.concurrency).is_equal_to("ci-${{ github.ref }}")

    def test_concurrency_object(self, minimal_job):
        w = parse_workflow(
            {
                "on": "push",
                "concurrency": {
                    "group": "ci-${{ github.ref }}",
                    "cancel-in-progress": True,
                },
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.concurrency).is_instance_of(Concurrency)
        assert_that(w.concurrency.cancel_in_progress).is_true()

    def test_permissions_global(self, minimal_job):
        w = parse_workflow({"on": "push", "permissions": "read-all", "jobs": {"build": minimal_job}})
        assert_that(w.permissions).is_equal_to(PermissionAccess.READ_ALL)

    def test_permissions_granular(self, minimal_job):
        w = parse_workflow(
            {
                "on": "push",
                "permissions": {
                    "contents": "read",
                    "pull-requests": "write",
                    "issues": "none",
                },
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.permissions).is_instance_of(PermissionsEvent)
        assert_that(w.permissions.contents).is_equal_to(PermissionLevel.READ)
        assert_that(w.permissions.pull_requests).is_equal_to(PermissionLevel.WRITE)
        assert_that(w.permissions.issues).is_equal_to(PermissionLevel.NONE)

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
