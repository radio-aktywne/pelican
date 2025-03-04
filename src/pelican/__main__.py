import typer

from pelican.api.app import AppBuilder
from pelican.cli import CliBuilder
from pelican.config.builder import ConfigBuilder
from pelican.config.errors import ConfigError
from pelican.console import FallbackConsoleBuilder
from pelican.server import Server
from pelican.services.graphite.migrator import GraphiteMigrator

cli = CliBuilder().build()


@cli.command()
def main() -> None:
    """Main entry point."""

    console = FallbackConsoleBuilder().build()

    try:
        config = ConfigBuilder().build()
    except ConfigError as ex:
        console.print("Failed to build config!")
        console.print_exception()
        raise typer.Exit(1) from ex

    try:
        app = AppBuilder(config).build()
    except Exception as ex:
        console.print("Failed to build app!")
        console.print_exception()
        raise typer.Exit(2) from ex

    try:
        GraphiteMigrator(config).migrate()
    except Exception as ex:
        console.print("Failed to apply graphite migrations!")
        console.print_exception()
        raise typer.Exit(3) from ex

    try:
        server = Server(app, config.server)
        server.run()
    except Exception as ex:
        console.print("Failed to run server!")
        console.print_exception()
        raise typer.Exit(4) from ex


if __name__ == "__main__":
    cli()
