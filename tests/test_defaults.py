from assertpy import assert_that
from pydantic import ValidationError

from ghanon.models.workflow import Defaults, DefaultsRun


class TestDefaults:
    def test_run_shell(self):
        defaults = Defaults.model_validate({"run": {"shell": "bash"}})

        assert defaults.run is not None
        assert_that(defaults.run.shell).is_equal_to("bash")

    def test_run_working_directory(self):
        defaults = Defaults.model_validate({"run": {"working-directory": "./app"}})

        assert defaults.run is not None
        assert_that(defaults.run.working_directory).is_equal_to("./app")

    def test_run_both(self):
        defaults = Defaults.model_validate({"run": {"shell": "pwsh", "working-directory": "./src"}})

        assert defaults.run is not None
        assert_that(defaults.run.shell).is_equal_to("pwsh")
        assert_that(defaults.run.working_directory).is_equal_to("./src")

    def test_run_requires_property(self):
        assert_that(DefaultsRun.model_validate).raises(ValidationError).when_called_with({})

    def test_defaults_requires_run(self):
        assert_that(Defaults.model_validate).raises(ValidationError).when_called_with({})
