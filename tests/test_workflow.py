"""Comprehensive tests for GitHub Actions Workflow Pydantic models using assertpy.

Run with: pytest test_workflow.py -v
Fast run:  pytest test_workflow.py -q --tb=short
"""

import pytest
from assertpy import assert_that
from pydantic import ValidationError

from ghanon.models.workflow import (
    BranchProtectionRuleEvent,
    CheckRunEvent,
    CheckSuiteEvent,
    # Supporting models
    Concurrency,
    Container,
    Defaults,
    DefaultsRun,
    DiscussionCommentEvent,
    DiscussionEvent,
    Environment,
    # Enums
    EventType,
    IssueCommentEvent,
    IssuesEvent,
    LabelEvent,
    Matrix,
    MergeGroupEvent,
    MilestoneEvent,
    # Main models
    NormalJob,
    # Event models
    OnConfiguration,
    PermissionAccess,
    PermissionLevel,
    PermissionsEvent,
    ProjectCardEvent,
    ProjectColumnEvent,
    ProjectEvent,
    # Activity types
    PullRequestActivityType,
    PullRequestEvent,
    PullRequestReviewCommentEvent,
    PullRequestReviewEvent,
    PullRequestTargetEvent,
    PushEvent,
    RegistryPackageEvent,
    ReleaseEvent,
    ReusableWorkflowCallJob,
    RunnerGroup,
    ScheduleItem,
    Step,
    Strategy,
    WorkflowCallEvent,
    WorkflowCallInputType,
    WorkflowDispatchEvent,
    # Input/output models
    WorkflowDispatchInput,
    WorkflowDispatchInputType,
    WorkflowRunActivityType,
    WorkflowRunEvent,
)
from ghanon.parser import parse_workflow, parse_workflow_yaml

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def minimal_job():
    """Minimal valid job configuration."""
    return {"runs-on": "ubuntu-latest", "steps": [{"run": "echo hello"}]}


@pytest.fixture
def minimal_workflow(minimal_job):
    """Minimal valid workflow."""
    return {"on": "push", "jobs": {"build": minimal_job}}


# =============================================================================
# Workflow Tests
# =============================================================================


class TestWorkflow:
    """Tests for the root Workflow model."""

    def test_minimal(self, minimal_workflow):
        w = parse_workflow(minimal_workflow)
        assert_that(w.on).is_equal_to(EventType.PUSH)
        assert_that(w.jobs).contains_key("build")

    def test_with_name(self, minimal_job):
        w = parse_workflow({"name": "CI", "on": "push", "jobs": {"build": minimal_job}})
        assert_that(w.name).is_equal_to("CI")

    def test_with_run_name(self, minimal_job):
        w = parse_workflow(
            {
                "name": "Deploy",
                "run-name": "Deploy by @${{ github.actor }}",
                "on": "push",
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.run_name).is_equal_to("Deploy by @${{ github.actor }}")

    def test_event_list(self, minimal_job):
        w = parse_workflow({"on": ["push", "pull_request"], "jobs": {"build": minimal_job}})
        assert_that(w.on).is_equal_to([EventType.PUSH, EventType.PULL_REQUEST])

    def test_env(self, minimal_job):
        w = parse_workflow(
            {
                "on": "push",
                "env": {"CI": "true", "NODE_VERSION": 18},
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.env).is_equal_to({"CI": "true", "NODE_VERSION": 18})

    def test_defaults(self, minimal_job):
        w = parse_workflow(
            {
                "on": "push",
                "defaults": {"run": {"shell": "bash", "working-directory": "./src"}},
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.defaults.run.shell).is_equal_to("bash")
        assert_that(w.defaults.run.working_directory).is_equal_to("./src")

    def test_concurrency_string(self, minimal_job):
        w = parse_workflow(
            {
                "on": "push",
                "concurrency": "ci-${{ github.ref }}",
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.concurrency).is_equal_to("ci-${{ github.ref }}")

    def test_concurrency_object(self, minimal_job):
        w = parse_workflow(
            {
                "on": "push",
                "concurrency": {
                    "group": "ci-${{ github.ref }}",
                    "cancel-in-progress": True,
                },
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.concurrency).is_instance_of(Concurrency)
        assert_that(w.concurrency.cancel_in_progress).is_true()

    def test_permissions_global(self, minimal_job):
        w = parse_workflow({"on": "push", "permissions": "read-all", "jobs": {"build": minimal_job}})
        assert_that(w.permissions).is_equal_to(PermissionAccess.READ_ALL)

    def test_permissions_granular(self, minimal_job):
        w = parse_workflow(
            {
                "on": "push",
                "permissions": {
                    "contents": "read",
                    "pull-requests": "write",
                    "issues": "none",
                },
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.permissions).is_instance_of(PermissionsEvent)
        assert_that(w.permissions.contents).is_equal_to(PermissionLevel.READ)
        assert_that(w.permissions.pull_requests).is_equal_to(PermissionLevel.WRITE)
        assert_that(w.permissions.issues).is_equal_to(PermissionLevel.NONE)

    def test_missing_on_fails(self, minimal_job):
        assert_that(parse_workflow).raises(ValidationError).when_called_with({"jobs": {"build": minimal_job}})

    def test_missing_jobs_fails(self):
        assert_that(parse_workflow).raises(ValidationError).when_called_with({"on": "push"})

    def test_empty_jobs_fails(self):
        assert_that(parse_workflow).raises(ValidationError).when_called_with({"on": "push", "jobs": {}})

    @pytest.mark.parametrize("invalid_id", ["123start", "-invalid", "has space", "has.dot"])
    def test_invalid_job_id_fails(self, invalid_id, minimal_job):
        assert_that(parse_workflow).raises(ValidationError).when_called_with(
            {"on": "push", "jobs": {invalid_id: minimal_job}},
        )

    @pytest.mark.parametrize("valid_id", ["build", "_private", "test_job", "job-1", "A1"])
    def test_valid_job_ids(self, valid_id, minimal_job):
        w = parse_workflow({"on": "push", "jobs": {valid_id: minimal_job}})
        assert_that(w.jobs).contains_key(valid_id)


# =============================================================================
# Job Tests
# =============================================================================


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


# =============================================================================
# Step Tests
# =============================================================================


class TestStep:
    """Tests for Step model."""

    def test_run_only(self):
        step = Step.model_validate({"run": "echo hello"})
        assert_that(step.run).is_equal_to("echo hello")

    def test_uses_only(self):
        step = Step.model_validate({"uses": "actions/checkout@v4"})
        assert_that(step.uses).is_equal_to("actions/checkout@v4")

    def test_requires_uses_or_run(self):
        assert_that(Step.model_validate).raises(ValidationError).when_called_with({"name": "Invalid"})

    def test_cannot_have_both(self):
        assert_that(Step.model_validate).raises(ValidationError).when_called_with(
            {"uses": "actions/checkout@v4", "run": "echo"},
        )

    def test_id(self):
        step = Step.model_validate({"id": "my-step", "run": "echo"})
        assert_that(step.id).is_equal_to("my-step")

    def test_name(self):
        step = Step.model_validate({"name": "Build", "run": "npm run build"})
        assert_that(step.name).is_equal_to("Build")

    def test_if_string(self):
        step = Step.model_validate({"run": "echo", "if": "success()"})
        assert_that(step.if_).is_equal_to("success()")

    def test_if_boolean(self):
        step = Step.model_validate({"run": "echo", "if": True})
        assert_that(step.if_).is_true()

    def test_with(self):
        step = Step.model_validate(
            {
                "uses": "actions/setup-node@v4",
                "with": {"node-version": "18", "cache": "npm"},
            },
        )
        assert_that(step.with_).contains_entry({"node-version": "18"})

    def test_env(self):
        step = Step.model_validate({"run": "echo $VAR", "env": {"VAR": "value"}})
        assert_that(step.env).contains_entry({"VAR": "value"})

    def test_shell(self):
        step = Step.model_validate({"run": "echo", "shell": "bash"})
        assert_that(step.shell).is_equal_to("bash")

    def test_working_directory(self):
        step = Step.model_validate({"run": "echo", "working-directory": "./app"})
        assert_that(step.working_directory).is_equal_to("./app")

    def test_shell_requires_run(self):
        assert_that(Step.model_validate).raises(ValidationError).when_called_with(
            {"uses": "actions/checkout@v4", "shell": "bash"},
        )

    def test_working_directory_requires_run(self):
        assert_that(Step.model_validate).raises(ValidationError).when_called_with(
            {"uses": "actions/checkout@v4", "working-directory": "./app"},
        )

    def test_continue_on_error(self):
        step = Step.model_validate({"run": "echo", "continue-on-error": True})
        assert_that(step.continue_on_error).is_true()

    def test_timeout_minutes(self):
        step = Step.model_validate({"run": "long-task", "timeout-minutes": 60})
        assert_that(step.timeout_minutes).is_equal_to(60)

    @pytest.mark.parametrize("shell", ["bash", "pwsh", "python", "sh", "cmd", "powershell"])
    def test_shell_types(self, shell):
        step = Step.model_validate({"run": "echo", "shell": shell})
        assert_that(step.shell).is_equal_to(shell)


# =============================================================================
# Event Tests
# =============================================================================


class TestPushEvent:
    """Tests for push event configuration."""

    def test_empty(self):
        e = PushEvent.model_validate({})
        assert_that(e.branches).is_none()

    def test_branches(self):
        e = PushEvent.model_validate({"branches": ["main", "develop"]})
        assert_that(e.branches).is_equal_to(["main", "develop"])

    def test_branches_ignore(self):
        e = PushEvent.model_validate({"branches-ignore": ["feature/*"]})
        assert_that(e.branches_ignore).is_equal_to(["feature/*"])

    def test_branches_exclusive(self):
        assert_that(PushEvent.model_validate).raises(ValidationError).when_called_with(
            {"branches": ["main"], "branches-ignore": ["dev"]},
        )

    def test_tags(self):
        e = PushEvent.model_validate({"tags": ["v*"]})
        assert_that(e.tags).is_equal_to(["v*"])

    def test_tags_ignore(self):
        e = PushEvent.model_validate({"tags-ignore": ["v0.*"]})
        assert_that(e.tags_ignore).is_equal_to(["v0.*"])

    def test_tags_exclusive(self):
        assert_that(PushEvent.model_validate).raises(ValidationError).when_called_with(
            {"tags": ["v*"], "tags-ignore": ["v0.*"]},
        )

    def test_paths(self):
        e = PushEvent.model_validate({"paths": ["src/**", "*.py"]})
        assert_that(e.paths).is_equal_to(["src/**", "*.py"])

    def test_paths_ignore(self):
        e = PushEvent.model_validate({"paths-ignore": ["docs/**", "*.md"]})
        assert_that(e.paths_ignore).is_equal_to(["docs/**", "*.md"])

    def test_paths_exclusive(self):
        assert_that(PushEvent.model_validate).raises(ValidationError).when_called_with(
            {"paths": ["src/**"], "paths-ignore": ["test/**"]},
        )


class TestPullRequestEvent:
    """Tests for pull_request event configuration."""

    def test_types(self):
        e = PullRequestEvent.model_validate({"types": ["opened", "synchronize", "reopened"]})
        assert_that(e.types).is_length(3)
        assert_that(e.types).contains(PullRequestActivityType.OPENED)

    def test_all_filters(self):
        e = PullRequestEvent.model_validate(
            {
                "types": ["opened"],
                "branches": ["main"],
                "paths": ["src/**"],
            },
        )
        assert_that(e.types).is_equal_to([PullRequestActivityType.OPENED])
        assert_that(e.branches).is_equal_to(["main"])
        assert_that(e.paths).is_equal_to(["src/**"])


class TestPullRequestTargetEvent:
    """Tests for pull_request_target event configuration."""

    def test_types(self):
        e = PullRequestTargetEvent.model_validate({"types": ["opened", "labeled"]})
        assert_that(e.types).is_length(2)

    def test_filter_exclusivity(self):
        assert_that(PullRequestTargetEvent.model_validate).raises(ValidationError).when_called_with(
            {
                "branches": ["main"],
                "branches-ignore": ["feature/*"],
            },
        )


class TestScheduleEvent:
    """Tests for schedule event configuration."""

    def test_single_cron(self):
        item = ScheduleItem.model_validate({"cron": "0 0 * * *"})
        assert_that(item.cron).is_equal_to("0 0 * * *")

    def test_in_workflow(self, minimal_job):
        w = parse_workflow(
            {
                "on": {"schedule": [{"cron": "0 0 * * *"}, {"cron": "0 12 * * 1-5"}]},
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.on.schedule).is_length(2)


class TestWorkflowDispatchEvent:
    """Tests for workflow_dispatch event configuration."""

    def test_empty(self):
        e = WorkflowDispatchEvent.model_validate({})
        assert_that(e.inputs).is_none()

    def test_string_input(self):
        e = WorkflowDispatchEvent.model_validate(
            {
                "inputs": {
                    "name": {
                        "description": "Name",
                        "type": "string",
                        "default": "world",
                    },
                },
            },
        )
        assert_that(e.inputs["name"].type).is_equal_to(WorkflowDispatchInputType.STRING)

    def test_boolean_input(self):
        e = WorkflowDispatchEvent.model_validate(
            {
                "inputs": {
                    "debug": {
                        "description": "Debug",
                        "type": "boolean",
                        "default": False,
                    },
                },
            },
        )
        assert_that(e.inputs["debug"].type).is_equal_to(WorkflowDispatchInputType.BOOLEAN)

    def test_choice_input(self):
        e = WorkflowDispatchEvent.model_validate(
            {
                "inputs": {
                    "env": {
                        "description": "Environment",
                        "type": "choice",
                        "options": ["dev", "staging", "prod"],
                    },
                },
            },
        )
        assert_that(e.inputs["env"].options).is_equal_to(["dev", "staging", "prod"])

    def test_choice_requires_options(self):
        assert_that(WorkflowDispatchInput.model_validate).raises(ValidationError).when_called_with(
            {
                "description": "Env",
                "type": "choice",
            },
        )

    def test_required_input(self):
        e = WorkflowDispatchEvent.model_validate(
            {
                "inputs": {"token": {"description": "API Token", "required": True}},
            },
        )
        assert_that(e.inputs["token"].required).is_true()


class TestWorkflowCallEvent:
    """Tests for workflow_call event configuration."""

    def test_inputs(self):
        e = WorkflowCallEvent.model_validate(
            {
                "inputs": {
                    "environment": {"type": "string", "required": True},
                    "debug": {"type": "boolean", "default": False},
                },
            },
        )
        assert_that(e.inputs["environment"].type).is_equal_to(WorkflowCallInputType.STRING)
        assert_that(e.inputs["debug"].default).is_false()

    def test_outputs(self):
        e = WorkflowCallEvent.model_validate(
            {
                "outputs": {
                    "version": {
                        "description": "The version",
                        "value": "${{ jobs.build.outputs.version }}",
                    },
                },
            },
        )
        assert_that(e.outputs).contains_key("version")

    def test_secrets(self):
        e = WorkflowCallEvent.model_validate(
            {
                "secrets": {
                    "API_KEY": {"description": "API key", "required": True},
                },
            },
        )
        assert_that(e.secrets["API_KEY"].required).is_true()


class TestWorkflowRunEvent:
    """Tests for workflow_run event configuration."""

    def test_types(self):
        e = WorkflowRunEvent.model_validate(
            {
                "types": ["completed"],
                "workflows": ["CI"],
            },
        )
        assert_that(e.types).contains(WorkflowRunActivityType.COMPLETED)

    def test_branches(self):
        e = WorkflowRunEvent.model_validate(
            {
                "workflows": ["Build"],
                "branches": ["main"],
            },
        )
        assert_that(e.branches).is_equal_to(["main"])


class TestActivityTypeEvents:
    """Tests for events with activity types."""

    @pytest.mark.parametrize(
        ("event_class", "types"),
        [
            (BranchProtectionRuleEvent, ["created", "edited", "deleted"]),
            (CheckRunEvent, ["created", "rerequested", "completed"]),
            (CheckSuiteEvent, ["completed", "requested"]),
            (DiscussionEvent, ["created", "answered"]),
            (DiscussionCommentEvent, ["created", "edited"]),
            (IssueCommentEvent, ["created", "deleted"]),
            (IssuesEvent, ["opened", "closed", "labeled"]),
            (LabelEvent, ["created", "deleted"]),
            (MergeGroupEvent, ["checks_requested"]),
            (MilestoneEvent, ["created", "closed"]),
            (ProjectEvent, ["created", "closed"]),
            (ProjectCardEvent, ["created", "moved"]),
            (ProjectColumnEvent, ["created", "moved"]),
            (PullRequestReviewEvent, ["submitted", "dismissed"]),
            (PullRequestReviewCommentEvent, ["created", "edited"]),
            (RegistryPackageEvent, ["published", "updated"]),
            (ReleaseEvent, ["published", "released"]),
        ],
    )
    def test_activity_types(self, event_class, types):
        e = event_class.model_validate({"types": types})
        assert_that(e.types).is_not_none()
        assert_that(e.types).is_length(len(types))


class TestOnConfiguration:
    """Tests for complete on configuration."""

    def test_multiple_events(self, minimal_job):
        w = parse_workflow(
            {
                "on": {
                    "push": {"branches": ["main"]},
                    "pull_request": {"branches": ["main"]},
                    "workflow_dispatch": {},
                },
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.on).is_instance_of(OnConfiguration)
        assert_that(w.on.push).is_not_none()
        assert_that(w.on.pull_request).is_not_none()
        assert_that(w.on.workflow_dispatch).is_not_none()

    def test_simple_events(self, minimal_job):
        w = parse_workflow(
            {
                "on": {"create": None, "delete": None, "fork": None},
                "jobs": {"build": minimal_job},
            },
        )
        assert_that(w.on).is_instance_of(OnConfiguration)


# =============================================================================
# Container Tests
# =============================================================================


class TestContainer:
    """Tests for Container model."""

    def test_image_only(self):
        c = Container.model_validate({"image": "node:18"})
        assert_that(c.image).is_equal_to("node:18")

    def test_with_credentials(self):
        c = Container.model_validate(
            {
                "image": "ghcr.io/owner/image",
                "credentials": {"username": "user", "password": "${{ secrets.TOKEN }}"},
            },
        )
        assert_that(c.credentials.username).is_equal_to("user")

    def test_with_env(self):
        c = Container.model_validate({"image": "node:18", "env": {"NODE_ENV": "test"}})
        assert_that(c.env).contains_entry({"NODE_ENV": "test"})

    def test_with_ports(self):
        c = Container.model_validate({"image": "nginx", "ports": [80, 443, "8080:80"]})
        assert_that(c.ports).is_length(3)

    def test_with_volumes(self):
        c = Container.model_validate(
            {
                "image": "node:18",
                "volumes": ["/tmp:/tmp", "my-vol:/data"],
            },
        )
        assert_that(c.volumes).is_length(2)

    def test_with_options(self):
        c = Container.model_validate({"image": "node:18", "options": "--cpus 2 --memory 4g"})
        assert_that(c.options).contains("--cpus")


# =============================================================================
# Defaults Tests
# =============================================================================


class TestDefaults:
    """Tests for Defaults model."""

    def test_run_shell(self):
        d = Defaults.model_validate({"run": {"shell": "bash"}})
        assert_that(d.run.shell).is_equal_to("bash")

    def test_run_working_directory(self):
        d = Defaults.model_validate({"run": {"working-directory": "./app"}})
        assert_that(d.run.working_directory).is_equal_to("./app")

    def test_run_both(self):
        d = Defaults.model_validate({"run": {"shell": "pwsh", "working-directory": "./src"}})
        assert_that(d.run.shell).is_equal_to("pwsh")
        assert_that(d.run.working_directory).is_equal_to("./src")

    def test_run_requires_property(self):
        assert_that(DefaultsRun.model_validate).raises(ValidationError).when_called_with({})

    def test_defaults_requires_run(self):
        assert_that(Defaults.model_validate).raises(ValidationError).when_called_with({})


# =============================================================================
# Concurrency Tests
# =============================================================================


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


# =============================================================================
# Environment Tests
# =============================================================================


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


# =============================================================================
# Permissions Tests
# =============================================================================


class TestPermissions:
    """Tests for Permissions model."""

    def test_all_permissions(self):
        p = PermissionsEvent.model_validate(
            {
                "actions": "read",
                "attestations": "write",
                "checks": "write",
                "contents": "read",
                "deployments": "write",
                "discussions": "read",
                "id-token": "write",
                "issues": "write",
                "models": "read",
                "packages": "write",
                "pages": "write",
                "pull-requests": "write",
                "repository-projects": "read",
                "security-events": "write",
                "statuses": "write",
            },
        )
        assert_that(p.actions).is_equal_to(PermissionLevel.READ)
        assert_that(p.id_token).is_equal_to(PermissionLevel.WRITE)
        assert_that(p.models).is_equal_to("read")  # models has restricted enum


# =============================================================================
# YAML Parsing Tests
# =============================================================================


class TestYamlParsing:
    """Tests for YAML parsing functionality."""

    def test_basic_yaml(self):
        yaml = """
name: CI
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Hello"
"""
        w = parse_workflow_yaml(yaml)
        assert_that(w.name).is_equal_to("CI")
        assert_that(w.jobs).contains_key("build")

    def test_on_boolean_fix(self):
        """Test that 'on' is not parsed as boolean True."""
        yaml = """
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo test
"""
        w = parse_workflow_yaml(yaml)
        assert_that(w.on).is_equal_to(EventType.PUSH)

    def test_complex_workflow(self):
        yaml = """
name: CI/CD
on:
  push:
    branches: [main, develop]
  pull_request:
  workflow_dispatch:
    inputs:
      deploy:
        description: Deploy after build
        type: boolean
        default: false

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

env:
  NODE_VERSION: '18'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run lint

  test:
    needs: lint
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: ['18', '20']
      fail-fast: false
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test

  deploy:
    needs: [lint, test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    steps:
      - run: echo "Deploying..."
"""
        w = parse_workflow_yaml(yaml)
        assert_that(w.name).is_equal_to("CI/CD")
        assert_that(w.jobs).is_length(3)
        assert_that(w.jobs["test"].needs).is_equal_to("lint")
        assert_that(w.jobs["deploy"].needs).is_equal_to(["lint", "test"])
        assert_that(w.jobs["test"].strategy.fail_fast).is_false()


# =============================================================================
# Round-trip Tests
# =============================================================================


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


# =============================================================================
# Edge Cases
# =============================================================================


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
