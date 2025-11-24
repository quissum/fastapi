import uuid

from fastapi_users import schemas


class SUserRead(schemas.BaseUser[uuid.UUID]):
    """What we send to the front (no password required)."""


class SUserCreate(schemas.BaseUserCreate):
    """What we accept during registration (email + password)."""


class SUserUpdate(schemas.BaseUserUpdate):
    """What can be updated in your profile."""
