"""Ghanon CLI implementation."""

import os
from pathlib import Path

import click
from pydantic_core import ErrorDetails

from ghanon.formatter import Formatter
from ghanon.logger import Logger
from ghanon.parser import ParsingResult, WorkflowParser

formatter = Formatter()
logger = Logger(formatter)


@click.command()
@click.argument("workflow", type=click.Path(), required=False)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
def main(workflow: str, verbose: bool) -> None:
    """Run Ghanon CLI."""
    if workflow:
        return validate_single_workflow(workflow, verbose)

    return validate_all_workflows()


def validate_single_workflow(workflow: str, verbose: bool) -> None:
    """Validate a single workflow file.

    Args:
        workflow: Path to the workflow file to validate.
        verbose: Whether to enable verbose output.

    """
    filepath = Path(workflow)

    if not filepath.is_file():
        logger.fatal(f"File '{filepath}' does not exist")

    if verbose:
        logger.info(f"Parsing workflow file: {filepath}")

    result = parse(filepath)

    if result.success:
        return logger.success(f"{filepath} is a valid workflow.")

    return handle_validation_errors(result, workflow)


def validate_all_workflows() -> None:
    """Validate all workflow files in .github/workflows directory."""
    workflows_dir = Path.cwd() / ".github" / "workflows"

    for workflow in workflows_dir.glob("*.yml"):
        result = parse(workflow)

        if result.success:
            logger.success(f"{workflow} is a valid workflow.")


def parse(filepath: Path) -> ParsingResult:
    """Parse a workflow file and return the parsing result."""
    parser = WorkflowParser()
    return parser.parse(filepath.read_text())


def log_validation_errors(result: ParsingResult, workflow: str) -> None:
    """Log validation errors without aborting.

    Args:
        result: Parsing result containing errors.
        workflow: Path to the workflow file being validated.

    """
    logger.error(f"Error parsing workflow file {workflow}. Found {len(result.errors)} error(s).{os.linesep}")
    for error in result.errors:
        msg = format_error(error, workflow, result.line_map)
        logger.log(msg, os.linesep)


def handle_validation_errors(result: ParsingResult, workflow: str) -> None:
    """Handle validation errors by logging them and aborting.

    Args:
        result: Parsing result containing errors.
        workflow: Path to the workflow file being validated.

    """
    log_validation_errors(result, workflow)

    raise click.Abort


def format_error(error: ErrorDetails, workflow: str, line_map: dict[str, int]) -> str:
    """Format a Pydantic error for display."""
    msg = error["msg"]
    loc = error["loc"]
    message = f"{formatter.bold(msg)} {os.linesep}  --> {formatter.warning(workflow)}"

    if not loc:
        return message

    location = ".".join(str(segment) for segment in loc) if isinstance(loc, tuple) else loc
    line_info = get_line_info(location, line_map)

    return f"{message}:{line_info} at `{location}`"


def get_line_info(location: str, line_map: dict[str, int]) -> int:
    """Get line number information for a given location path.

    Finds the most specific (longest) matching path in the line map.
    This helps point to the deepest nested field causing validation errors.

    Args:
        location: Dotted path location from error details.
        line_map: Dictionary mapping paths to line numbers.

    Returns:
        Line number suffix (e.g., ":42") or empty string if not found.

    """
    # Pydantic error locations include model class names not present in the YAML line map,
    # so we search for partial path matches by progressively shortening the location path.
    # Valid errors always have at least one matching partial path (e.g., root keys like "on", "jobs").
    path_parts = location.split(".")
    for i in range(len(path_parts), 0, -1):
        partial_path = ".".join(path_parts[:i])
        if partial_path in line_map:
            return line_map[partial_path]

    # Fallback for edge cases where no path matches (should not occur with valid workflow errors)
    return 0  # pragma: no cover
