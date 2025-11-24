import uuid

from sqlalchemy import case, exists, func, select, text

from app.db.models.task import MTask
from app.db.session import new_session
from app.schemas.task import STaskAdd, STaskUpdate


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd, user_id: uuid.UUID) -> int:
        async with new_session() as session:
            data_dict = data.model_dump()
            task = MTask(**data_dict, user_id=user_id)
            session.add(task)
            await session.flush()
            await session.commit()

            return task.id

    @classmethod
    async def get_list_tasks(
        cls, q: str | None, limit: int, offset: int, user_id: uuid.UUID
    ) -> tuple[list[MTask], int]:
        async with new_session() as session:
            stmt = select(MTask).where(MTask.user_id == user_id)

            if q and q.strip().startswith("#"):
                tag_value = q.strip()[1:]
                pattern = f"%{tag_value}%"

                tags_lateral = text(
                    "jsonb_array_elements_text(tasks.meta->'tags') AS tag(tag)"
                )

                stmt = stmt.where(
                    MTask.meta.is_not(None),
                    exists(
                        select(1)
                        .select_from(tags_lateral)
                        .where(text("tag ILIKE :pattern"))
                    ),
                ).params(pattern=pattern)
                stmt = stmt.order_by(MTask.updated_at.desc())
            elif q:
                pattern = f"%{q.strip()}%"
                stmt = stmt.where(
                    MTask.name.ilike(pattern) | MTask.content.ilike(pattern)
                )
                name_first = case((MTask.name.ilike(pattern), 0), else_=1)
                stmt = stmt.order_by(name_first, MTask.updated_at.desc())
            else:
                stmt = stmt.order_by(MTask.updated_at.desc())

            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = (await session.execute(count_stmt)).scalar_one()

            stmt = stmt.offset(offset).limit(limit)
            result = await session.execute(stmt)
            task_models = result.scalars().all()

            return task_models, total

    @classmethod
    async def count_all(cls) -> int:
        async with new_session() as session:
            result = await session.execute(select(func.count(MTask.id)))
            return result.scalar_one()

    @classmethod
    async def get_one(cls, id: int, user_id: uuid.UUID) -> MTask | None:
        async with new_session() as session:
            result = await session.execute(
                select(MTask).where(MTask.id == id, MTask.user_id == user_id)
            )
            return result.scalar_one_or_none()

    @classmethod
    async def delete_one(cls, id: int, user_id: uuid.UUID) -> bool:
        async with new_session() as session:
            result = await session.execute(
                select(MTask).where(MTask.id == id, MTask.user_id == user_id)
            )
            task = result.scalar_one_or_none()

            if task is None:
                return False

            await session.delete(task)
            await session.commit()
            return True

    @classmethod
    async def update_one(
        cls, id: int, patch: STaskUpdate, user_id: uuid.UUID
    ) -> bool:
        async with new_session() as session:
            result = await session.execute(
                select(MTask).where(MTask.id == id, MTask.user_id == user_id)
            )
            task = result.scalar_one_or_none()

            if task is None:
                return False

            data = patch.model_dump(exclude_unset=True, exclude_none=True)

            for field, value in data.items():
                setattr(task, field, value)

            await session.commit()
            return True
