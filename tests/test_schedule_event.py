from typing import Any

from assertpy import assert_that

from ghanon.models.workflow import OnConfiguration, ScheduleItem
from ghanon.parser import parse_workflow


class TestScheduleEvent:
    """Tests for schedule event configuration."""

    def test_single_cron(self):
        pattern = "0 0 * * *"
        item = ScheduleItem.model_validate({"cron": pattern})
        assert_that(item.cron).is_equal_to(pattern)

    def test_in_workflow(self, minimal_job: dict[str, Any]):
        patterns = [{"cron": "0 0 * * *"}, {"cron": "0 12 * * 1-5"}]
        workflow = parse_workflow(
            {
                "on": {"schedule": patterns},
                "jobs": {"build": minimal_job},
            },
        )

        assert isinstance(workflow.on, OnConfiguration)
        assert isinstance(workflow.on.schedule, list)
        assert_that(workflow.on.schedule[0].cron).is_equal_to("0 0 * * *")
        assert_that(workflow.on.schedule[1].cron).is_equal_to("0 12 * * 1-5")
