"""Entry point for Ghanon command-line interface."""

import os
import sys
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


def get_line_info(location: str, line_map: dict[str, int]) -> str:
    """Get line number information for a given location path.

    Tries exact match first, then falls back to partial path matching
    to handle union type discriminators in Pydantic error paths.

    Args:
        location: Dotted path location from error details.
        line_map: Dictionary mapping paths to line numbers.

    Returns:
        Line number suffix (e.g., ":42") or empty string if not found.

    """
    if location in line_map:
        return f":{line_map[location]}"

    # Try to find the best partial match
    # Remove union type discriminators and try again
    path_parts = location.split(".")
    for i in range(len(path_parts), 0, -1):
        partial_path = ".".join(path_parts[:i])
        if partial_path in line_map:
            return f":{line_map[partial_path]}"

    return ""


def format_error(error: ErrorDetails, workflow: str, line_map: dict[str, int]) -> str:
    """Format a Pydantic error for display."""
    msg = error["msg"]
    loc = error["loc"]
    message = f"{msg} {os.linesep}  --> {workflow}"

    if not loc:
        return message

    location = ".".join(str(segment) for segment in loc) if isinstance(loc, tuple) else loc
    line_info = get_line_info(location, line_map)

    return f"{message}{line_info} at `{location}`"


if __name__ == "__main__":
    sys.exit(main())
