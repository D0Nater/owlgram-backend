"""Session CRUD."""

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from owlgram.core.exceptions.session import SessionNotFoundException
from owlgram.core.security import JWT
from owlgram.lib.models import SessionModel
from owlgram.lib.schemas.enums.redis import SessionRedisKeyType
from owlgram.lib.schemas.session import SessionCreateResponseSchema, SessionCreateSchema, SessionRedisData


async def get_session_model(db: AsyncSession, session_id: int) -> SessionModel:
    """Retrieve a session model from the database.

    Args:
        db (AsyncSession): The asynchronous SQLAlchemy session to use for the query.
        session_id (int): The ID of the session to retrieve.

    Returns:
        SessionModel: The retrieved SessionModel object.

    Raises:
        SessionNotFoundException: If no session with the given ID is found.
    """
    query = select(SessionModel).where(SessionModel.id == session_id)
    result = (await db.execute(query)).scalar_one_or_none()

    if result is None:
        raise SessionNotFoundException(session_id=session_id)

    return result


async def create_session(
    db: AsyncSession, redis: Redis, jwt: JWT, schema: SessionCreateSchema
) -> SessionCreateResponseSchema:
    """Create a session.

    Args:
        db (AsyncSession): The asynchronous SQLAlchemy session to use for the query.
        redis (Redis): The Redis client to use for caching the session.
        jwt (JWT): The JWT utility for encoding session tokens.
        schema (SessionCreateSchema): The schema containing session creation data.

    Returns:
        SessionCreateResponseSchema: The response schema containing the session token.
    """
    session_model = SessionModel(**schema.model_dump())
    db.add(session_model)
    await db.flush()

    await redis.set(
        SessionRedisKeyType.session.format(session_id=session_model.id),
        SessionRedisData(username=session_model.username).model_dump_json(),
    )

    return SessionCreateResponseSchema.model_construct(token=jwt.encode(data=session_model.id))


async def delete_session(db: AsyncSession, redis: Redis, session_id: int) -> None:
    """Delete a session from Database and Redis.

    Args:
        db (AsyncSession): The asynchronous SQLAlchemy session to use for the query.
        redis (Redis): The Redis client to use for deleting the session.
        session_id (int): The ID of the session to delete.

    Returns:
        None
    """
    session_model = await get_session_model(db, session_id)
    await db.delete(session_model)

    await redis.delete(SessionRedisKeyType.session.format(session_id=session_id))
