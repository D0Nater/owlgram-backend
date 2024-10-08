"""Dependency injection annotations for the agent module."""

from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import ConnectionPool, Redis as AbstractRedis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from owlgram.core.config import AppConfig
from owlgram.core.security import JWT
from owlgram.lib.schemas.session import SessionData

from . import constructors as app_depends


def app_config_stub() -> AppConfig:
    """Get app config stub."""
    raise NotImplementedError


def jwt(config: Annotated[AppConfig, Depends(app_config_stub)]) -> JWT:
    """Get JWT."""
    return app_depends.jwt(config)


def db_session_maker_stub() -> sessionmaker[Any]:
    """Get database session maker stub."""
    raise NotImplementedError


async def db_session(
    request: Request,
    maker: Annotated[sessionmaker[Any], Depends(db_session_maker_stub)],
) -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    generator = app_depends.db_session_autocommit(maker)
    session = await anext(generator)
    request.state.db = session

    yield session

    try:
        await anext(generator)
    except StopAsyncIteration:
        pass
    else:
        raise RuntimeError("Database session not closed (db dependency generator is not closed).")


def redis_conn_pool_stub() -> ConnectionPool:
    """Get redis connection pool stub."""
    raise NotImplementedError


async def redis_conn(
    request: Request,
    conn_pool: Annotated[ConnectionPool, Depends(redis_conn_pool_stub)],
) -> AsyncGenerator[AbstractRedis, None]:
    """Get redis connection."""
    generator = app_depends.redis_conn(conn_pool)
    redis = await anext(generator)
    request.state.redis = redis

    yield redis

    try:
        await anext(generator)
    except StopAsyncIteration:
        pass
    else:
        raise RuntimeError("Redis session not closed (redis dependency generator is not closed).")


async def get_session_data(
    jwt: Annotated[JWT, Depends(jwt)],
    redis: Annotated[AbstractRedis, Depends(redis_conn)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
) -> SessionData:
    """Get session data."""
    return await app_depends.get_session_data(jwt, redis, credentials.credentials)


AppConfigDependency = Annotated[AppConfig, Depends(app_config_stub)]
DatabaseDependency = Annotated[AsyncSession, Depends(db_session)]
RedisDependency = Annotated[AbstractRedis, Depends(redis_conn)]
JWTDependency = Annotated[JWT, Depends(jwt)]
SessionDataDependency = Annotated[SessionData, Depends(get_session_data)]
