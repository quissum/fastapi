from fastapi import APIRouter

from app.core.auth import auth_backend, fastapi_users
from app.schemas.user import SUserCreate, SUserRead, SUserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(SUserRead, SUserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(SUserRead, SUserUpdate),
    prefix="/users",
    tags=["users"],
)
