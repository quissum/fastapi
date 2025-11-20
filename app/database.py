import uuid
from datetime import datetime
from typing import Any
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost:5432/tasks",
    echo=False
)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class MTask(Model):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    content: Mapped[str | None] = mapped_column(nullable=True)

    created_at: Mapped[int] = mapped_column(
        default=lambda: int(datetime.now().timestamp())
    )
    updated_at: Mapped[int] = mapped_column(
        default=lambda: int(datetime.now().timestamp()),
        onupdate=lambda: int(datetime.now().timestamp())
    )

    meta: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
