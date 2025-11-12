from sqlalchemy import select
from database import MTask, new_session
from schemas import STask, STaskAdd


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
    async def get_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(MTask)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_shemas = [STask.model_validate(
                task_model, from_attributes=True) for task_model in task_models]

            return task_shemas
