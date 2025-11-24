from pydantic import BaseModel


class STaskMeta(BaseModel):
    tags: list[str] = []
    deleted: bool = False
    archived: bool = False
    pinned: bool = False


class STaskAdd(BaseModel):
    name: str
    content: str | None = None
    meta: STaskMeta | None = None


class STaskOut(STaskAdd):
    id: int
    created_at: int
    updated_at: int

    model_config = {"from_attributes": True}


class STaskPage(BaseModel):
    items: list[STaskOut]
    offset: int
    limit: int
    total: int


class STaskId(BaseModel):
    ok: bool = True
    task_id: int


class STaskUpdate(BaseModel):
    name: str | None = None
    content: str | None = None
    meta: STaskMeta | None = None
