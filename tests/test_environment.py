"""Tests for Environment model."""

from assertpy import assert_that
from pydantic import ValidationError

from ghanon.models.workflow import Environment


class TestEnvironment:
    """Tests for Environment model."""

    def test_name_only(self):
        e = Environment.model_validate({"name": "production"})
        assert_that(e.name).is_equal_to("production")

    def test_with_url(self):
        e = Environment.model_validate({"name": "staging", "url": "https://staging.example.com"})
        assert_that(e.url).is_equal_to("https://staging.example.com")

    def test_name_required(self):
        assert_that(Environment.model_validate).raises(ValidationError).when_called_with({"url": "https://example.com"})
