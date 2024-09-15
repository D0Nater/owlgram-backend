"""Module with main CLI function."""

import click

from owlgram.lib.utils.log import configure_logging


@click.group()
def cli() -> None:
    """Control interface for Owlgram."""
    configure_logging()
