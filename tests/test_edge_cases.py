"""Tests for edge cases and special scenarios."""

from assertpy import assert_that

from ghanon.models.workflow import NormalJob, Step
from ghanon.parser import parse_workflow


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_expression_in_env(self, minimal_job):
        w = parse_workflow(
            {
                "on": "push",
                "env": "${{ fromJson(needs.setup.outputs.env) }}",
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.env).contains("${{")

    def test_expression_in_runs_on(self):
        job = NormalJob.model_validate({"runs-on": "${{ matrix.os }}"})
        assert_that(job.runs_on).is_equal_to("${{ matrix.os }}")

    def test_expression_in_timeout(self):
        job = NormalJob.model_validate(
            {
                "runs-on": "ubuntu-latest",
                "timeout-minutes": "${{ inputs.timeout }}",
            },
        )
        assert_that(job.timeout_minutes).contains("${{")

    def test_multiline_run(self):
        step = Step.model_validate(
            {
                "run": """
echo "Line 1"
echo "Line 2"
echo "Line 3"
""",
            },
        )
        assert_that(step.run).contains("Line 1")
        assert_that(step.run).contains("Line 3")

    def test_special_characters_in_name(self, minimal_job):
        w = parse_workflow(
            {
                "name": "CI: Build & Test (v2.0)",
                "on": "push",
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.name).contains("&")
