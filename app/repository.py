from sqlalchemy import case, exists, func, select, text
from .database import MTask, new_session
from .schemas import STaskAdd, STaskUpdate


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            data_dict = data.model_dump()
            task = MTask(**data_dict)
            session.add(task)
            await session.flush()
            await session.commit()

            return task.id

    @classmethod
    async def get_list_tasks(cls, q: str | None, limit: int, offset: int) -> list[MTask]:
        async with new_session() as session:
            stmt = select(MTask)

            if q and q.strip().startswith("#"):
                tag_value = q.strip()[1:]
                pattern = f"%{tag_value}%"

                tags_lateral = text(
                    "jsonb_array_elements_text(tasks.meta->'tags') AS tag(tag)")

                stmt = stmt.where(
                    MTask.meta.is_not(None),
                    exists(
                        select(1)
                        .select_from(tags_lateral)
                        .where(text("tag ILIKE :pattern"))
                    )
                ).params(pattern=pattern)
                stmt = stmt.order_by(MTask.updated_at.desc())
            elif q:
                pattern = f"%{q.strip()}%"
                stmt = stmt.where(MTask.name.ilike(pattern) |
                                  MTask.content.ilike(pattern))
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
    async def get_one(cls, id: int) -> MTask | None:
        async with new_session() as session:
            result = await session.get(MTask, id)
            return result

    @classmethod
    async def delete_one(cls, id: int) -> bool:
        async with new_session() as session:
            task = await session.get(MTask, id)

            if task is None:
                return False

            await session.delete(task)
            await session.commit()
            return True

    @classmethod
    async def update_one(cls, id: int, patch: STaskUpdate) -> bool:
        async with new_session() as session:
            task = await session.get(MTask, id)

            if task is None:
                return False

            data = patch.model_dump(exclude_unset=True, exclude_none=True)

            for field, value in data.items():
                setattr(task, field, value)

            await session.commit()
            return True
