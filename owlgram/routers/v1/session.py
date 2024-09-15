"""Session endpoint."""

from fastapi import APIRouter

from owlgram.core.dependencies import DatabaseDependency, JWTDependency, RedisDependency, SessionDataDependency
from owlgram.core.exceptions.session import SessionNotFoundException
from owlgram.lib.db import session as session_db
from owlgram.lib.schemas.session import SessionCreateResponseSchema, SessionCreateSchema
from owlgram.lib.utils.openapi import exc_list


router = APIRouter(tags=["session"], prefix="/session")


@router.post("/", response_model=SessionCreateResponseSchema)
async def create_session(
    db: DatabaseDependency, redis: RedisDependency, jwt: JWTDependency, schema: SessionCreateSchema
) -> SessionCreateResponseSchema:
    """Create session."""
    return await session_db.create_session(db, redis, jwt, schema)


@router.delete("/", status_code=204, openapi_extra=exc_list(SessionNotFoundException))
async def delete_session(db: DatabaseDependency, redis: RedisDependency, session_data: SessionDataDependency) -> None:
    """Delete session."""
    return await session_db.delete_session(db, redis, session_data.session_id)
