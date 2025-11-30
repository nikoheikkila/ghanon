from pathlib import Path

from assertpy import assert_that

from ghanon.models.matrix import Strategy
from ghanon.models.workflow import EventType
from ghanon.parser import parse_workflow_yaml


class TestYamlParsing:
    def test_basic_yaml(self):
        yaml = self.load_fixture("basic_yaml.yml")

        workflow = parse_workflow_yaml(yaml)

        assert_that(workflow.name).is_equal_to("CI")
        assert_that(workflow.jobs).contains_key("build")

    def test_on_boolean_fix(self):
        yaml = self.load_fixture("on_boolean_fix.yml")

        workflow = parse_workflow_yaml(yaml)

        assert_that(workflow.on).is_equal_to(EventType.PUSH)

    def test_complex_workflow(self):
        yaml = self.load_fixture("complex_workflow.yml")

        workflow = parse_workflow_yaml(yaml)

        assert isinstance(workflow.jobs["test"].strategy, Strategy)
        assert_that(workflow.name).is_equal_to("CI/CD")
        assert_that(workflow.jobs).is_length(3)
        assert_that(workflow.jobs["lint"].needs).is_none()
        assert_that(workflow.jobs["test"].needs).is_equal_to("lint")
        assert_that(workflow.jobs["test"].strategy.fail_fast).is_false()
        assert_that(workflow.jobs["deploy"].needs).is_equal_to(["lint", "test"])

    def load_fixture(self, filename: str) -> str:
        fixture_path = Path(__file__).parent / "fixtures" / filename
        return fixture_path.read_text()
