from typing import Annotated
from fastapi import APIRouter, Depends
from repository import TaskRepository
from schemas import STask, STaskAdd, STaskId


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post('')
async def add_task(task: Annotated[STaskAdd, Depends()]) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {'ok': True, 'task_id': task_id}


@router.get('')
async def get_tasks() -> list[STask]:
    task_schemes = await TaskRepository.get_all()
    return task_schemes
