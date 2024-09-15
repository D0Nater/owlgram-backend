"""App dependencies."""

from typing import Annotated

from redis.asyncio import Redis as AbstractRedis
from sqlalchemy.ext.asyncio import AsyncSession

from owlgram.core.config import AppConfig
from owlgram.core.security import JWT
from owlgram.lib.schemas.session import SessionData

from . import fastapi


AppConfigDependency = Annotated[AppConfig, *fastapi.AppConfigDependency.__metadata__]
DatabaseDependency = Annotated[AsyncSession, *fastapi.DatabaseDependency.__metadata__]
RedisDependency = Annotated[AbstractRedis, *fastapi.RedisDependency.__metadata__]
JWTDependency = Annotated[JWT, *fastapi.JWTDependency.__metadata__]
SessionDataDependency = Annotated[SessionData, *fastapi.SessionDataDependency.__metadata__]

__all__ = [
    "AppConfigDependency",
    "DatabaseDependency",
    "RedisDependency",
    "JWTDependency",
    "SessionDataDependency",
]
