from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.auth import current_active_user
from app.db.models.user import MUser
from app.repositories.task import TaskRepository
from app.schemas.task import STaskAdd, STaskId, STaskOut, STaskPage, STaskUpdate


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=STaskId)
async def add_task(
    task: STaskAdd,
    user: MUser = Depends(current_active_user),
) -> STaskId:
    task_id = await TaskRepository.add_one(task, user.id)
    return STaskId(task_id=task_id)


@router.get("/", response_model=STaskPage)
async def get_list_tasks(
    q: str | None = Query(None, min_length=1),
    limit: int = Query(20, ge=0, le=100),
    offset: int = Query(0, ge=0),
    user: MUser = Depends(current_active_user),
) -> STaskPage:
    task_models, total = await TaskRepository.get_list_tasks(q, limit, offset, user.id)
    task_schemas = [STaskOut.model_validate(task_model) for task_model in task_models]

    return STaskPage(items=task_schemas, offset=offset, limit=limit, total=total)


@router.get("/{task_id}", response_model=STaskOut)
async def get_task(task_id: int, user: MUser = Depends(current_active_user)) -> STaskOut:
    task_model = await TaskRepository.get_one(task_id, user.id)

    if task_model is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return STaskOut.model_validate(task_model)


@router.patch("/{task_id}", response_model=STaskId)
async def update_task(
    task_id: int,
    patch: STaskUpdate,
    user: MUser = Depends(current_active_user),
) -> STaskId:
    is_updated = await TaskRepository.update_one(task_id, patch, user.id)

    if not is_updated:
        raise HTTPException(status_code=404, detail="Task not found")

    return STaskId(task_id=task_id)


@router.delete("/{task_id}", response_model=STaskId)
async def delete_task(
    task_id: int, user: MUser = Depends(current_active_user)
) -> STaskId:
    is_deleted = await TaskRepository.delete_one(task_id, user.id)

    if not is_deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return STaskId(task_id=task_id)
