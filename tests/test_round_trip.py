"""Tests for model serialization round-trips."""

from assertpy import assert_that

from ghanon.parser import parse_workflow


class TestRoundTrip:
    """Tests for model serialization round-trips."""

    def test_workflow_to_dict(self, minimal_workflow):
        w = parse_workflow(minimal_workflow)
        d = w.model_dump(by_alias=True, exclude_none=True)
        assert_that(d).contains_key("on")
        assert_that(d).contains_key("jobs")

    def test_workflow_round_trip(self, minimal_workflow):
        w1 = parse_workflow(minimal_workflow)
        d = w1.model_dump(by_alias=True, exclude_none=True)
        w2 = parse_workflow(d)
        assert_that(w1.on).is_equal_to(w2.on)
        assert_that(list(w1.jobs.keys())).is_equal_to(list(w2.jobs.keys()))

    def test_complex_round_trip(self):
        data = {
            "name": "Test",
            "on": {"push": {"branches": ["main"]}, "pull_request": {}},
            "concurrency": {"group": "ci", "cancel-in-progress": True},
            "jobs": {
                "build": {
                    "runs-on": "ubuntu-latest",
                    "strategy": {"matrix": {"node": ["18", "20"]}},
                    "steps": [
                        {"uses": "actions/checkout@v4"},
                        {"run": "npm test", "shell": "bash"},
                    ],
                },
            },
        }
        w1 = parse_workflow(data)
        d = w1.model_dump(by_alias=True, exclude_none=True)
        w2 = parse_workflow(d)
        assert_that(w1.name).is_equal_to(w2.name)
        assert_that(w1.jobs["build"].strategy.matrix.model_extra).is_equal_to(
            w2.jobs["build"].strategy.matrix.model_extra,
        )
