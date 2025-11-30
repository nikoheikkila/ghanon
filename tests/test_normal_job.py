"""Tests for NormalJob model."""

from assertpy import assert_that

from ghanon.models.workflow import Container, Environment, NormalJob, RunnerGroup


class TestNormalJob:
    """Tests for NormalJob model."""

    def test_minimal(self):
        job = NormalJob.model_validate({"runs-on": "ubuntu-latest"})
        assert_that(job.runs_on).is_equal_to("ubuntu-latest")

    def test_with_steps(self):
        job = NormalJob.model_validate(
            {
                "runs-on": "ubuntu-latest",
                "steps": [{"run": "echo test"}],
            },
        )
        assert_that(job.steps).is_length(1)

    def test_name(self):
        job = NormalJob.model_validate({"name": "Build Job", "runs-on": "ubuntu-latest"})
        assert_that(job.name).is_equal_to("Build Job")

    def test_needs_single(self):
        job = NormalJob.model_validate({"runs-on": "ubuntu-latest", "needs": "build"})
        assert_that(job.needs).is_equal_to("build")

    def test_needs_multiple(self):
        job = NormalJob.model_validate({"runs-on": "ubuntu-latest", "needs": ["build", "test"]})
        assert_that(job.needs).is_equal_to(["build", "test"])

    def test_if_condition(self):
        job = NormalJob.model_validate(
            {
                "runs-on": "ubuntu-latest",
                "if": "github.ref == 'refs/heads/main'",
            },
        )
        assert_that(job.if_).is_equal_to("github.ref == 'refs/heads/main'")

    def test_environment_string(self):
        job = NormalJob.model_validate({"runs-on": "ubuntu-latest", "environment": "production"})
        assert_that(job.environment).is_equal_to("production")

    def test_environment_object(self):
        job = NormalJob.model_validate(
            {
                "runs-on": "ubuntu-latest",
                "environment": {"name": "production", "url": "https://example.com"},
            },
        )
        assert_that(job.environment).is_instance_of(Environment)
        assert_that(job.environment.name).is_equal_to("production")

    def test_outputs(self):
        job = NormalJob.model_validate(
            {
                "runs-on": "ubuntu-latest",
                "outputs": {"version": "${{ steps.get_version.outputs.version }}"},
            },
        )
        assert_that(job.outputs).contains_key("version")

    def test_env(self):
        job = NormalJob.model_validate(
            {
                "runs-on": "ubuntu-latest",
                "env": {"DEBUG": "true", "PORT": 3000},
            },
        )
        assert_that(job.env).contains_entry({"DEBUG": "true"})
        assert_that(job.env).contains_entry({"PORT": 3000})

    def test_timeout_minutes(self):
        job = NormalJob.model_validate({"runs-on": "ubuntu-latest", "timeout-minutes": 30})
        assert_that(job.timeout_minutes).is_equal_to(30)

    def test_continue_on_error(self):
        job = NormalJob.model_validate({"runs-on": "ubuntu-latest", "continue-on-error": True})
        assert_that(job.continue_on_error).is_true()

    def test_container_string(self):
        job = NormalJob.model_validate({"runs-on": "ubuntu-latest", "container": "node:18"})
        assert_that(job.container).is_equal_to("node:18")

    def test_container_object(self):
        job = NormalJob.model_validate(
            {
                "runs-on": "ubuntu-latest",
                "container": {
                    "image": "node:18",
                    "env": {"NODE_ENV": "test"},
                    "ports": [80, "443:443"],
                    "volumes": ["/tmp:/tmp"],
                    "options": "--cpus 2",
                },
            },
        )
        assert_that(job.container).is_instance_of(Container)
        assert_that(job.container.image).is_equal_to("node:18")
        assert_that(job.container.ports).is_equal_to([80, "443:443"])

    def test_services(self):
        job = NormalJob.model_validate(
            {
                "runs-on": "ubuntu-latest",
                "services": {
                    "postgres": {
                        "image": "postgres:15",
                        "env": {"POSTGRES_PASSWORD": "test"},
                    },
                    "redis": {"image": "redis:7"},
                },
            },
        )
        assert_that(job.services).contains_key("postgres")
        assert_that(job.services).contains_key("redis")

    def test_runs_on_array(self):
        job = NormalJob.model_validate({"runs-on": ["self-hosted", "linux", "x64"]})
        assert_that(job.runs_on).is_equal_to(["self-hosted", "linux", "x64"])

    def test_runs_on_group(self):
        job = NormalJob.model_validate(
            {
                "runs-on": {"group": "large-runners", "labels": ["ubuntu-latest"]},
            },
        )
        assert_that(job.runs_on).is_instance_of(RunnerGroup)

    def test_runs_on_expression(self):
        job = NormalJob.model_validate({"runs-on": "${{ matrix.os }}"})
        assert_that(job.runs_on).is_equal_to("${{ matrix.os }}")
