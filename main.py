"""Entry point for Ghanon command-line interface."""

import sys
from pathlib import Path

import click
import yaml
from pydantic import ValidationError

from ghanon.parser import parse_workflow_yaml

custom_errors = {
    "model_type": "This is not a GitHub Actions workflow",
}


@click.command()
@click.argument("workflow", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
def main(workflow: str, verbose: bool) -> int:
    """Run the Ghanon CLI."""
    filepath = Path(workflow)

    if verbose:
        click.echo(f"Parsing workflow file: {filepath}")

    try:
        parse_workflow_yaml(filepath.read_text())
        click.echo(f"{filepath} is a valid workflow.")
    except yaml.YAMLError as e:
        click.echo(f"Error parsing YAML in {filepath}: {e}")
        raise click.Abort from e
    except ValidationError as e:
        click.echo(f"Error parsing {filepath}. Found {e.error_count()} error(s).")
        raise click.Abort from e

    return 0


if __name__ == "__main__":
    sys.exit(main())
