import uuid
from typing import AsyncGenerator, Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions, models
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.core.config import settings
from app.db.models.user import MUser
from app.db.session import new_session


async def get_user_db() -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    async with new_session() as session:
        yield SQLAlchemyUserDatabase(session, MUser)


class UserManager(UUIDIDMixin, BaseUserManager[MUser, uuid.UUID]):
    reset_password_token_secret = settings.reset_secret
    verification_token_secret = settings.verify_secret

    async def validate_password(
        self, password: str, user: Optional[models.UP] = None
    ) -> None:
        if len(password) < 8:
            raise exceptions.InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )

    async def on_after_register(
        self, user: MUser, request: Optional[Request] = None
    ) -> None:
        # In production, send email or trigger other side effects
        print(f"New user registered: {user.id}")


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)
