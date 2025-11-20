from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from .repository import TaskRepository
from .schemas import STaskOut, STaskAdd, STaskId, STaskPage, STaskUpdate


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post('/', response_model=STaskId)
async def add_task(task: Annotated[STaskAdd, Depends()]) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return STaskId(task_id=task_id)


@router.get('/', response_model=STaskPage)
async def get_list_tasks(
    q: str | None = Query(None, min_length=1),
    limit: int = Query(20, ge=0, le=100),
    offset: int = Query(0, ge=0)
) -> STaskPage:
    task_models, total = await TaskRepository.get_list_tasks(q, limit, offset)
    task_shemas = [STaskOut.model_validate(
        task_model) for task_model in task_models]

    return STaskPage(items=task_shemas,
                     offset=offset,
                     limit=limit,
                     total=total)


@router.get('/count', response_model=int)
async def count_all() -> int:
    return await TaskRepository.count_all()


@router.get('/{task_id}', response_model=STaskOut)
async def get_task(task_id: int) -> STaskOut:
    task_model = await TaskRepository.get_one(task_id)

    if task_model is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task_shema = STaskOut.model_validate(task_model)
    return task_shema


@router.put('/{task_id}', response_model=STaskId)
async def update_task(task_id: int, patch: Annotated[STaskUpdate, Depends()]) -> STaskId:
    is_updated = await TaskRepository.update_one(task_id, patch)

    if not is_updated:
        raise HTTPException(status_code=404, detail="Task not found")

    return STaskId(task_id=task_id)


@router.delete('/{task_id}', response_model=STaskId)
async def delete_task(task_id: int) -> STaskId:
    is_deleted = await TaskRepository.delete_one(task_id)

    if not is_deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return STaskId(task_id=task_id)
