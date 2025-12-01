"""Parser functions for GitHub Actions Workflow schema."""

from __future__ import annotations

from dataclasses import dataclass, field

import yaml
from pydantic_core import ErrorDetails, ValidationError

from .domain.workflow import Workflow

__all__ = [
    "ParsingResult",
    "WorkflowParser",
]


@dataclass
class ParsingResult:
    """Result of parsing a GitHub Actions workflow."""

    workflow: Workflow | None = None
    success: bool = False
    errors: list[ErrorDetails] = field(default_factory=list)

    @classmethod
    def with_success(cls, workflow: Workflow) -> ParsingResult:
        """Create a successful ParsingResult."""
        return cls(workflow=workflow, success=True, errors=[])

    @classmethod
    def with_errors(cls, error: ValidationError) -> ParsingResult:
        """Create a failed ParsingResult."""
        return cls(workflow=None, success=False, errors=error.errors())


class WorkflowParser:
    """Parser for GitHub Actions Workflows."""

    def parse(self, yaml_content: str) -> ParsingResult:
        """Parse a workflow dictionary into a ParsingResult."""
        data = yaml.safe_load(yaml_content)

        # Handle YAML 1.1 quirk: 'on' key is parsed as boolean True
        # This is a known issue with GitHub Actions workflows
        if True in data:
            data["on"] = data.pop(True)

        try:
            workflow = Workflow.model_validate(data)
            return ParsingResult.with_success(workflow)
        except ValidationError as error:
            return ParsingResult.with_errors(error)
