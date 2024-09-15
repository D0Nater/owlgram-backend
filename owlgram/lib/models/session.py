"""Session model."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .abc import AbstractModel


class SessionModel(AbstractModel):
    """Session model."""

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column("id", Integer(), primary_key=True, autoincrement=True)
    """Session ID."""

    username: Mapped[str] = mapped_column("username", String(64), nullable=False)
    """Username."""

    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    """Session creation timestamp."""
