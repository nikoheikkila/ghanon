"""Feature: GitHub Actions Workflow Validation with Ghanon"""

from pathlib import Path

import pytest
from assertpy import assert_that
from click import Command
from click.testing import CliRunner

from ghanon.cli import main


@pytest.fixture
def runner() -> CliRunner:
    """Fixture providing a Click CLI test runner."""
    return CliRunner()


def find(name: str) -> str:
    """Fixture providing the path to the workflow file."""
    return str(Path(__file__).parent / "fixtures" / name)


class TestValidCases:
    """Scenario Outline: Valid Cases"""

    def test_cli_help(self, runner: CliRunner):
        result = runner.invoke(main, args=["--help"])

        assert_that(result).has_exit_code(0)
        assert_that(result.output).snapshot("test_cli_help_output")

    @pytest.mark.parametrize("workflow", ["simple_workflow.yml", "complex_workflow.yml"])
    def test_valid_workflow(self, runner: CliRunner, workflow: str):
        result = runner.invoke(main, args=[find(workflow)])

        assert_that(result).has_exit_code(0)
        assert_that(result.output).matches(r"is a valid workflow")

    def test_valid_workflow_with_verbose(self, runner: CliRunner):
        result = runner.invoke(main, args=["--verbose", find("complex_workflow.yml")])

        assert_that(result).has_exit_code(0)
        assert_that(result.output).matches(r"Parsing workflow file")


class TestErrorCases:
    """Scenario Outline: Error Cases"""

    @pytest.mark.parametrize(
        ("workflow", "expected_error"),
        [
            (find("invalid_key.yml"), r"Error parsing workflow file"),
            (
                find("branch_trigger.yml"),
                r"Use the `pull_request` trigger instead of the `push\.branches` trigger",
            ),
            (
                find("secrets_inherit.yml"),
                r"Do not use `secrets: inherit` with reusable workflows as it can be insecure",
            ),
            (
                find("no_permissions.yml"),
                r"Jobs should specify `contents: read` permission at minimum "
                r"to satisfy the principle of least privilege",
            ),
            (
                find("no_permissions_reusable_job.yml"),
                r"Reusable workflow jobs should specify `contents: read` permission at minimum "
                r"to satisfy the principle of least privilege",
            ),
            ("nonexistent.yml", r"File 'nonexistent.yml' does not exist"),
            ("README.md", r"Input should be a valid dictionary or instance of Workflow"),
            ("pyproject.toml", r"Error parsing YAML"),
        ],
    )
    def test_raises_error(self, runner: CliRunner, workflow: str, expected_error: str):
        assert isinstance(main, Command)

        result = runner.invoke(main, args=[workflow])

        assert_that(result).has_exit_code(1)
        assert_that(result.output).matches(expected_error)
