from pathlib import Path

import pytest
from assertpy import assert_that
from click.testing import CliRunner, Result

from ghanon.cli import main

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def runner() -> CliRunner:
    """Fixture providing a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def valid_workflow() -> str:
    """Get path to a valid workflow file."""
    return str(FIXTURES_DIR / "complex_workflow.yml")


@pytest.fixture
def invalid_workflow() -> str:
    """Get path to an invalid workflow file."""
    return str(FIXTURES_DIR / "invalid_runner.yml")


@pytest.fixture
def invalid_yaml_file() -> str:
    """Get path to a workflow file with invalid YAML."""
    return str(FIXTURES_DIR / "invalid.yml")


class TestCLI:
    def test_cli_help(self, runner: CliRunner):
        result = runner.invoke(main, args=["--help"])

        self.assert_success(result, "Run Ghanon CLI.")
        self.assert_success(result, r"-v, --verbose\s+Enable verbose output.")
        self.assert_success(result, r"--help\s+Show this message and exit.")

    def test_valid_workflow(self, runner: CliRunner, valid_workflow: str):
        result = runner.invoke(main, args=[valid_workflow])

        self.assert_success(result, "is a valid workflow")

    def test_valid_workflow_with_verbose(self, runner: CliRunner, valid_workflow: str):
        result = runner.invoke(main, args=["--verbose", valid_workflow])

        self.assert_success(result, "Parsing workflow file")

    def test_invalid_workflow_reports_errors(self, runner: CliRunner, invalid_workflow: str):
        result = runner.invoke(main, args=[invalid_workflow])

        self.assert_failure(result, "Error parsing workflow file")

    def test_nonexistent_file(self, runner: CliRunner):
        result = runner.invoke(main, args=["nonexistent.yml"])

        self.assert_failure(result, "File 'nonexistent.yml' does not exist", exit_code=2)

    def test_workflow_with_a_markdown_file(self, runner: CliRunner):
        result = runner.invoke(main, args=["README.md"])

        self.assert_failure(result, "Input should be a valid dictionary or instance of Workflow")

    def test_workflow_with_a_toml_file(self, runner: CliRunner):
        result = runner.invoke(main, args=["pyproject.toml"])

        self.assert_failure(result, "Error parsing YAML")

    def assert_success(self, result: Result, message: str) -> None:
        assert_that(result.exit_code).is_equal_to(0)
        assert_that(result.output).matches(message)

    def assert_failure(self, result: Result, message: str, exit_code=1) -> None:
        assert_that(result.exit_code).is_equal_to(exit_code)
        assert_that(result.output).matches(message)
