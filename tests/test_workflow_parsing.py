"""Feature: GitHub Actions Workflow Validation"""

import re
from pathlib import Path

from assertpy import assert_that

from ghanon.domain.workflow import Workflow
from ghanon.parser import ParsingResult, WorkflowParser


class TestYamlParsing:
    parser = WorkflowParser()

    def test_very_complex_workflow_snapshot(self):
        """Scenario: Complex workflow validation"""
        yaml = self.read_file("complex_workflow.yml")

        result = self.parse(yaml)

        self.assert_result_was_success(result, snapshot_id="test_very_complex_workflow_snapshot")

    def test_workflow_with_push_branches_trigger_fails_validation(self):
        """Scenario: Fail for using branch trigger"""
        expected_error = r"Use the `pull_request` trigger instead of the `push\.branches` trigger\."
        yaml = self.read_file("workflow_with_push_branches.yml")

        result = self.parse(yaml)

        self.assert_result_has_error(result, expected_error)

    def read_file(self, filename: str) -> str:
        fixture_path = Path(__file__).parent / "fixtures" / filename
        return fixture_path.read_text()

    def parse(self, content: str) -> ParsingResult:
        return self.parser.parse(content)

    def assert_result_was_success(self, result: ParsingResult, snapshot_id: str | None = None) -> None:
        assert isinstance(result.workflow, Workflow)
        assert_that(result.success, "Expected success to be True").is_true()
        assert_that(result.errors, "Expected errors to be an empty list").is_empty()
        assert_that(result.workflow.model_dump_json(), "Expected data to match snapshot").snapshot(snapshot_id)

    def assert_result_has_error(self, result: ParsingResult, pattern: str) -> None:
        errors = [error["msg"] for error in result.errors]
        matched = any(re.search(pattern, error) for error in errors)

        assert_that(result.workflow, "Expected data to be None").is_none()
        assert_that(result.success, "Expected success to be False").is_false()
        assert_that(matched, f"No errors matching pattern: {pattern}").is_true()
