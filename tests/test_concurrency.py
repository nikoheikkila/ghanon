"""Tests for Concurrency model."""

from assertpy import assert_that
from pydantic import ValidationError

from ghanon.models.workflow import Concurrency


class TestConcurrency:
    """Tests for Concurrency model."""

    def test_group_only(self):
        c = Concurrency.model_validate({"group": "ci-${{ github.ref }}"})
        assert_that(c.group).is_equal_to("ci-${{ github.ref }}")
        assert_that(c.cancel_in_progress).is_none()

    def test_with_cancel(self):
        c = Concurrency.model_validate({"group": "deploy", "cancel-in-progress": True})
        assert_that(c.cancel_in_progress).is_true()

    def test_cancel_expression(self):
        c = Concurrency.model_validate(
            {
                "group": "ci",
                "cancel-in-progress": "${{ github.event_name == 'pull_request' }}",
            },
        )
        assert_that(c.cancel_in_progress).contains("${{")

    def test_group_required(self):
        assert_that(Concurrency.model_validate).raises(ValidationError).when_called_with({"cancel-in-progress": True})
