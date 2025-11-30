from pathlib import Path

from assertpy import assert_that

from ghanon.parser import parse_workflow_yaml


class TestYamlParsing:
    def test_very_complex_workflow_snapshot(self):
        yaml = self.load_fixture("complex_workflow.yml")

        workflow = parse_workflow_yaml(yaml)
        dump = workflow.model_dump_json()

        assert_that(dump).snapshot("test_very_complex_workflow_snapshot")

    def load_fixture(self, filename: str) -> str:
        fixture_path = Path(__file__).parent / "fixtures" / filename
        return fixture_path.read_text()
