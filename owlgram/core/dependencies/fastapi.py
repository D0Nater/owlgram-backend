"""Dependency injection annotations for the agent module."""

from typing import Annotated

from fastapi import Depends

from owlgram.core.config import AppConfig


def app_config_stub() -> AppConfig:
    """Get app config stub."""
    raise NotImplementedError


AppConfigDependency = Annotated[AppConfig, Depends(app_config_stub)]
