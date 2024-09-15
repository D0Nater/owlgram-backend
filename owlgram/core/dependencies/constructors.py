"""App dependencies constructors."""

from json import loads as json_loads
from typing import Any, AsyncGenerator, Generator

from jwt import InvalidTokenError
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from owlgram.core.config import AppConfig
from owlgram.core.exceptions.abc import UnauthorizedException
from owlgram.core.security import JWT
from owlgram.lib.schemas.enums.redis import SessionRedisKeyType
from owlgram.lib.schemas.session import SessionData


def config() -> AppConfig:
    """Get application config."""
    return AppConfig.from_env()


def jwt(config: AppConfig) -> JWT:
    """Get JWT."""
    return JWT(config.jwt.secret_key, config.jwt.algorithm)


def db_url(config: AppConfig) -> str:
    """Get database engine string."""
    return config.database.url


def db_engine(database_url: str) -> AsyncEngine:
    """Create database engine."""
    return create_async_engine(database_url, isolation_level="SERIALIZABLE")


def db_session_maker(
    engine: AsyncEngine | str,
) -> Generator[sessionmaker[Any], None, None]:
    """Create database session maker."""
    engine = engine if isinstance(engine, AsyncEngine) else db_engine(engine)
    maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore[call-overload]
    yield maker
    maker.close_all()


async def db_session(maker: sessionmaker[Any]) -> AsyncGenerator[AsyncSession, None]:
    """Create database session."""
    session = maker()
    try:
        yield session
    except SQLAlchemyError:
        await session.rollback()
        raise
    finally:
        await session.close()


async def db_session_autocommit(
    maker: sessionmaker[Any],
) -> AsyncGenerator[AsyncSession, None]:
    """Create database session with auto commit on successful execution."""
    session = maker()
    try:
        yield session
    except SQLAlchemyError:
        await session.rollback()
        raise
    else:
        await session.commit()
    finally:
        await session.close()


def redis_url(config: AppConfig) -> str:
    """Get Redis URL."""
    return config.redis.url


async def redis_pool(redis_url: str) -> AsyncGenerator[ConnectionPool, None]:
    """Create Redis connection pool."""
    pool = ConnectionPool.from_url(redis_url)
    yield pool
    await pool.disconnect()


async def redis_conn(pool: ConnectionPool) -> AsyncGenerator[Redis, None]:
    """Create Redis connection."""
    conn = Redis(connection_pool=pool)
    try:
        yield conn
    finally:
        await conn.close()


async def get_session_data(jwt: JWT, redis: Redis, token: str) -> SessionData:
    """Get session data."""
    payload = _decode_jwt(jwt, token)
    session_id: str | None = payload.get("sub")

    if session_id is None or not session_id.isdigit():
        raise UnauthorizedException(detail_="Invalid token")

    str_data = await redis.get(SessionRedisKeyType.session.format(session_id=session_id))

    if str_data is None:
        raise UnauthorizedException(detail_="Invalid token")

    return SessionData.model_construct(**json_loads(str_data), session_id=int(session_id))


def _decode_jwt(jwt: JWT, token: str) -> dict[str, Any]:
    """Decode JWT."""
    try:
        return jwt.decode(token)
    except InvalidTokenError:
        raise UnauthorizedException(detail_="Invalid token")
