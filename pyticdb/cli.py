"""Console script for pyticdb."""
import sys

import click


@click.command()
def main(args=None):
    """Console script for pyticdb."""
    click.echo(
        "Replace this message by putting your code into " "pyticdb.cli.main"
    )
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
