"""Ghanon CLI implementation."""

import os
from pathlib import Path

import click
from pydantic_core import ErrorDetails

from ghanon.parser import WorkflowParser


@click.command()
@click.argument("workflow", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
def main(workflow: str, verbose: bool) -> None:
    """Run Ghanon CLI."""
    filepath = Path(workflow)
    parser = WorkflowParser()

    if verbose:
        click.echo(f"Parsing workflow file: {filepath}")

    result = parser.parse(filepath.read_text())

    if result.success:
        return click.echo(f"{filepath} is a valid workflow.")

    click.echo(f"Error parsing {filepath}. Found {len(result.errors)} error(s).{os.linesep}")
    for error in result.errors:
        msg = format_error(error, workflow, result.line_map)
        click.echo(msg)
        click.echo(os.linesep)

    raise click.Abort


def format_error(error: ErrorDetails, workflow: str, line_map: dict[str, int]) -> str:
    """Format a Pydantic error for display."""
    msg = error["msg"]
    loc = error["loc"]
    message = f"{msg} {os.linesep}  --> {workflow}"

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
