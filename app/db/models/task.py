import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Model


class MTask(Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str]
    content: Mapped[str | None] = mapped_column(nullable=True)

    created_at: Mapped[int] = mapped_column(
        default=lambda: int(datetime.now().timestamp())
    )
    updated_at: Mapped[int] = mapped_column(
        default=lambda: int(datetime.now().timestamp()),
        onupdate=lambda: int(datetime.now().timestamp()),
    )

    meta: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
