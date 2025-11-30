"""Tests for Step model."""

import pytest
from assertpy import assert_that
from pydantic import ValidationError

from ghanon.models.workflow import Step


class TestStep:
    """Tests for Step model."""

    def test_run_only(self):
        step = Step.model_validate({"run": "echo hello"})
        assert_that(step.run).is_equal_to("echo hello")

    def test_uses_only(self):
        step = Step.model_validate({"uses": "actions/checkout@v4"})
        assert_that(step.uses).is_equal_to("actions/checkout@v4")

    def test_requires_uses_or_run(self):
        assert_that(Step.model_validate).raises(ValidationError).when_called_with({"name": "Invalid"})

    def test_cannot_have_both(self):
        assert_that(Step.model_validate).raises(ValidationError).when_called_with(
            {"uses": "actions/checkout@v4", "run": "echo"},
        )

    def test_id(self):
        step = Step.model_validate({"id": "my-step", "run": "echo"})
        assert_that(step.id).is_equal_to("my-step")

    def test_name(self):
        step = Step.model_validate({"name": "Build", "run": "npm run build"})
        assert_that(step.name).is_equal_to("Build")

    def test_if_string(self):
        step = Step.model_validate({"run": "echo", "if": "success()"})
        assert_that(step.if_).is_equal_to("success()")

    def test_if_boolean(self):
        step = Step.model_validate({"run": "echo", "if": True})
        assert_that(step.if_).is_true()

    def test_with(self):
        step = Step.model_validate(
            {
                "uses": "actions/setup-node@v4",
                "with": {"node-version": "18", "cache": "npm"},
            },
        )
        assert_that(step.with_).contains_entry({"node-version": "18"})

    def test_env(self):
        step = Step.model_validate({"run": "echo $VAR", "env": {"VAR": "value"}})
        assert_that(step.env).contains_entry({"VAR": "value"})

    def test_shell(self):
        step = Step.model_validate({"run": "echo", "shell": "bash"})
        assert_that(step.shell).is_equal_to("bash")

    def test_working_directory(self):
        step = Step.model_validate({"run": "echo", "working-directory": "./app"})
        assert_that(step.working_directory).is_equal_to("./app")

    def test_shell_requires_run(self):
        assert_that(Step.model_validate).raises(ValidationError).when_called_with(
            {"uses": "actions/checkout@v4", "shell": "bash"},
        )

    def test_working_directory_requires_run(self):
        assert_that(Step.model_validate).raises(ValidationError).when_called_with(
            {"uses": "actions/checkout@v4", "working-directory": "./app"},
        )

    def test_continue_on_error(self):
        step = Step.model_validate({"run": "echo", "continue-on-error": True})
        assert_that(step.continue_on_error).is_true()

    def test_timeout_minutes(self):
        step = Step.model_validate({"run": "long-task", "timeout-minutes": 60})
        assert_that(step.timeout_minutes).is_equal_to(60)

    @pytest.mark.parametrize("shell", ["bash", "pwsh", "python", "sh", "cmd", "powershell"])
    def test_shell_types(self, shell):
        step = Step.model_validate({"run": "echo", "shell": shell})
        assert_that(step.shell).is_equal_to(shell)
