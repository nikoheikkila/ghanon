"""Feature: GitHub Actions Workflow Validation"""

from pathlib import Path

import pytest
from assertpy import assert_that
from pydantic import ValidationError

from ghanon.parser import parse_workflow_yaml


class TestYamlParsing:
    def test_very_complex_workflow_snapshot(self):
        """Scenario: Complex workflow validation"""
        yaml = self.load_fixture("complex_workflow.yml")

        workflow = self.parse(yaml)
        dump = workflow.model_dump_json()

        assert_that(dump).snapshot("test_very_complex_workflow_snapshot")

    def test_workflow_with_push_branches_trigger_fails_validation(self):
        """Scenario: Fail for using branch trigger"""
        yaml = self.load_fixture("workflow_with_push_branches.yml")

        self.assert_failure(
            yaml,
            match=r"Use the `pull_request` trigger instead of the `push\.branches` trigger",
        )

    def assert_failure(self, yaml: str, match: str):
        with pytest.raises(ValidationError, match=match):
            self.parse(yaml)

    def parse(self, yaml: str):
        return parse_workflow_yaml(yaml)

    def load_fixture(self, filename: str) -> str:
        fixture_path = Path(__file__).parent / "fixtures" / filename
        return fixture_path.read_text()
