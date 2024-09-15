"""Redis key types."""

from .abc import BaseEnum


class BaseRedisKeyType(BaseEnum):
    """Redis key type."""

    @property
    def _prefix(self) -> str:
        raise NotImplementedError


class SessionRedisKeyType(BaseRedisKeyType):
    """Session redis key type."""

    _prefix = "session"

    session: str = f"{_prefix}:{{session_id}}"
    """Key for session."""
