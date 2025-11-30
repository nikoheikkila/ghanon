"""Parser functions for GitHub Actions Workflow schema."""

from __future__ import annotations

from typing import Any

import yaml

from .domain.workflow import Workflow

__all__ = [
    "parse_workflow",
    "parse_workflow_yaml",
]


def parse_workflow(data: dict[str, Any]) -> Workflow:
    """Parse a workflow dictionary into a Workflow model.

    Args:
        data: Dictionary representation of a GitHub Actions workflow

    Returns:
        Validated Workflow instance

    Raises:
        pydantic.ValidationError: If the workflow data is invalid

    """
    return Workflow.model_validate(data)


def parse_workflow_yaml(yaml_content: str) -> Workflow:
    """Parse a YAML string into a Workflow model.

    Args:
        yaml_content: YAML string representation of a GitHub Actions workflow

    Returns:
        Validated Workflow instance

    Raises:
        pydantic.ValidationError: If the workflow data is invalid
        yaml.YAMLError: If the YAML is malformed

    Note:
        Requires PyYAML to be installed.
        Handles the YAML 1.1 quirk where 'on' is parsed as boolean True.

    """
    data = yaml.safe_load(yaml_content)

    # Handle YAML 1.1 quirk: 'on' key is parsed as boolean True
    # This is a known issue with GitHub Actions workflows
    if True in data:
        data["on"] = data.pop(True)

    return parse_workflow(data)
