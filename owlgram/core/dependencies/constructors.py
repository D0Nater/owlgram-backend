"""App dependencies constructors."""

from owlgram.core.config import AppConfig


def config() -> AppConfig:
    """Get application config."""
    return AppConfig.from_env()
