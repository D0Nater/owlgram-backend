"""Session schemas for the API."""

from jwt import encode as jwt_encode

from . import fields as f
from .abc import BaseSchema


USERNAME = f.BaseField(description="Username.", min_length=1, max_length=64, examples=["Anonim"])
SESSION_ID = f.UUID(description="Session ID.")
TOKEN = f.BaseField(description="JSON Web Token.", examples=[jwt_encode({"sub": "1"}, "SECRET_KEY")])


class SessionRedisData(BaseSchema):
    """Session redis schema."""

    username: str


class SessionData(BaseSchema):
    """Session data."""

    session_id: int
    username: str


class SessionCreateSchema(BaseSchema):
    """Session create schema."""

    username: str = USERNAME


class SessionCreateResponseSchema(BaseSchema):
    """Session create response schema."""

    token: str = TOKEN
