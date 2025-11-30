"""Tests for ReusableWorkflowCallJob model."""

from assertpy import assert_that

from ghanon.models.workflow import ReusableWorkflowCallJob


class TestReusableWorkflowCallJob:
    """Tests for ReusableWorkflowCallJob model."""

    def test_minimal(self):
        job = ReusableWorkflowCallJob.model_validate(
            {
                "uses": "owner/repo/.github/workflows/workflow.yml@main",
            },
        )
        assert_that(job.uses).contains("workflow.yml")

    def test_with_inputs(self):
        job = ReusableWorkflowCallJob.model_validate(
            {
                "uses": "owner/repo/.github/workflows/workflow.yml@v1",
                "with": {"environment": "production", "debug": True},
            },
        )
        assert_that(job.with_).contains_entry({"environment": "production"})

    def test_secrets_inherit(self):
        job = ReusableWorkflowCallJob.model_validate(
            {
                "uses": "owner/repo/.github/workflows/workflow.yml@main",
                "secrets": "inherit",
            },
        )
        assert_that(job.secrets).is_equal_to("inherit")

    def test_secrets_explicit(self):
        job = ReusableWorkflowCallJob.model_validate(
            {
                "uses": "owner/repo/.github/workflows/workflow.yml@main",
                "secrets": {"API_KEY": "${{ secrets.API_KEY }}"},
            },
        )
        assert_that(job.secrets).contains_key("API_KEY")

    def test_with_strategy(self):
        job = ReusableWorkflowCallJob.model_validate(
            {
                "uses": "./.github/workflows/reusable.yml",
                "strategy": {"matrix": {"env": ["dev", "staging"]}},
            },
        )
        assert_that(job.strategy).is_not_none()
