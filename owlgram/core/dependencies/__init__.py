"""App dependencies."""

from typing import Annotated

from owlgram.core.config import AppConfig

from . import fastapi


AppConfigDependency = Annotated[AppConfig, *fastapi.AppConfigDependency.__metadata__]

__all__ = [
    "AppConfigDependency",
]
