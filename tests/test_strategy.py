"""Tests for Strategy and Matrix models."""

from assertpy import assert_that

from ghanon.models.workflow import Matrix, Strategy


class TestStrategy:
    """Tests for Strategy and Matrix models."""

    def test_simple_matrix(self):
        s = Strategy.model_validate({"matrix": {"os": ["ubuntu-latest", "windows-latest"]}})
        assert_that(s.matrix).is_instance_of(Matrix)

    def test_matrix_with_include(self):
        s = Strategy.model_validate(
            {
                "matrix": {
                    "os": ["ubuntu-latest"],
                    "node": ["18", "20"],
                    "include": [{"os": "ubuntu-latest", "node": "21", "experimental": True}],
                },
            },
        )
        assert_that(s.matrix.include).is_not_none()

    def test_matrix_with_exclude(self):
        s = Strategy.model_validate(
            {
                "matrix": {
                    "os": ["ubuntu-latest", "windows-latest"],
                    "node": ["18", "20"],
                    "exclude": [{"os": "windows-latest", "node": "18"}],
                },
            },
        )
        assert_that(s.matrix.exclude).is_not_none()

    def test_fail_fast(self):
        s = Strategy.model_validate({"matrix": {"os": ["ubuntu-latest"]}, "fail-fast": False})
        assert_that(s.fail_fast).is_false()

    def test_max_parallel(self):
        s = Strategy.model_validate({"matrix": {"os": ["ubuntu-latest"]}, "max-parallel": 2})
        assert_that(s.max_parallel).is_equal_to(2)

    def test_matrix_expression(self):
        s = Strategy.model_validate({"matrix": "${{ fromJson(needs.setup.outputs.matrix) }}"})
        assert_that(s.matrix).is_instance_of(str)
