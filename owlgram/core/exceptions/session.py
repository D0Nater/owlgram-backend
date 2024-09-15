"""Session-related exceptions."""

from .abc import AbstractException, NotFoundException


class SessionException(AbstractException):
    """Base session exception."""


class SessionNotFoundException(SessionException, NotFoundException):
    """Session not found."""

    auto_additional_info_fields = ["session_id"]

    detail = "Session {session_id} not found"
