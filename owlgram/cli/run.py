"""Server launch related commands."""

import os

import click
import uvicorn

from .cli import cli


@cli.command()
@click.option("--host", "-h", default="127.0.0.1", help="Host to bind to.")
@click.option("--port", "-p", default=8000, help="Port to bind to.")
@click.option("--reload", "-r", is_flag=True, help="Reload on code changes.")
@click.option("--workers", "-w", default=1, help="Number of workers.")
@click.option("--env", "-e", multiple=True, help="Environment variables.")
def run(host: str, port: int, reload: bool, workers: int, env: list[str]) -> None:
    """Run the API webserver."""
    for key, value in [item.split("=") for item in env]:
        os.environ[key.upper()] = value
    uvicorn.run(
        "owlgram.app:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        factory=True,
    )


@cli.command()
@click.option("--docker", is_flag=True, help="If this is a docker container.")
def dev(docker: bool) -> None:
    """Run the development server with pre-defined settings."""
    os.environ["PRODUCTION"] = os.environ.get("PRODUCTION", "false")

    uvicorn.run(
        "owlgram.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        workers=1,
        factory=True,
    )
